#!/usr/bin/env python3
"""Scan source files for common motion craft failures.

This is a lightweight guardrail, not a substitute for reviewing motion in a
browser. It catches the mistakes Tastemaker should never ship by accident:
unbounded transitions, sluggish easing, impossible scale origins, layout
animation, long UI durations, hover motion without pointer gating, and movement
without reduced-motion handling.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


EXTENSIONS = {
    ".css",
    ".html",
    ".js",
    ".jsx",
    ".mjs",
    ".ts",
    ".tsx",
    ".vue",
    ".svelte",
}

SKIP_DIRS = {
    ".git",
    ".netlify",
    ".playwright-cli",
    "node_modules",
    "dist",
    "build",
    "coverage",
}

LAYOUT_PROPERTIES = (
    "width",
    "height",
    "margin",
    "padding",
    "top",
    "right",
    "bottom",
    "left",
    "inset",
    "border-radius",
    "box-shadow",
)


@dataclass
class Finding:
    severity: str
    path: Path
    line: int
    rule: str
    message: str


def iter_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix in EXTENSIONS:
            files.append(path)
            continue
        if not path.is_dir():
            continue
        for child in path.rglob("*"):
            if any(part in SKIP_DIRS for part in child.parts):
                continue
            if child.is_file() and child.suffix in EXTENSIONS:
                files.append(child)
    return sorted(set(files))


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def add_regex_findings(
    findings: list[Finding],
    path: Path,
    text: str,
    pattern: str,
    severity: str,
    rule: str,
    message: str,
    flags: int = re.IGNORECASE,
) -> None:
    for match in re.finditer(pattern, text, flags):
        findings.append(Finding(severity, path, line_number(text, match.start()), rule, message))


def audit_file(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    findings: list[Finding] = []

    has_motion = bool(re.search(r"\b(transition|animation|gsap\.|animate\(|@keyframes|ScrollTrigger|motion\.)\b", text))
    has_reduced_motion = "prefers-reduced-motion" in text or "useReducedMotion" in text or "matchMedia" in text
    has_hover_motion = bool(re.search(r":hover[^{]*\{[^}]*\b(transform|animation|transition)\b", text, re.I | re.S))
    has_pointer_gate = "@media (hover: hover)" in text or "@media(hover:hover)" in text

    add_regex_findings(
        findings,
        path,
        text,
        r"transition\s*:\s*all\b",
        "HIGH",
        "transition-all",
        "Avoid `transition: all`; name transform, opacity, color, or background explicitly.",
    )
    add_regex_findings(
        findings,
        path,
        text,
        r"\bease-in\b",
        "HIGH",
        "ease-in-ui",
        "Avoid `ease-in` for UI motion; use a strong ease-out for entrances and responses.",
    )
    add_regex_findings(
        findings,
        path,
        text,
        r"scale(?:3d|X|Y)?\(\s*0(?:\.0+)?\s*\)",
        "HIGH",
        "scale-zero",
        "Avoid `scale(0)`; start near `scale(0.95)` with opacity.",
    )
    add_regex_findings(
        findings,
        path,
        text,
        r"transform-origin\s*:\s*center",
        "MEDIUM",
        "origin-center",
        "`transform-origin: center` is wrong for trigger-anchored popovers, menus, and tooltips. Confirm this is a modal or change it.",
    )

    transition_prop_pattern = r"transition(?:-property)?\s*:\s*([^;\n}]+)"
    for match in re.finditer(transition_prop_pattern, text, re.I):
        value = match.group(1)
        for prop in LAYOUT_PROPERTIES:
            if re.search(rf"\b{re.escape(prop)}\b", value, re.I):
                findings.append(
                    Finding(
                        "HIGH",
                        path,
                        line_number(text, match.start()),
                        "layout-transition",
                        f"Transition includes `{prop}`; prefer transform or opacity.",
                    )
                )

    duration_context = re.compile(
        r"(?:transition|animation|duration|delay)[^;\n}]*?(?<![\w.])(\d+(?:\.\d+)?|\.\d+)(ms|s)\b",
        re.I,
    )
    for match in duration_context.finditer(text):
        amount = float(match.group(1))
        unit = match.group(2).lower()
        ms = amount * 1000 if unit == "s" else amount
        if 300 < ms <= 2000:
            findings.append(
                Finding(
                    "MEDIUM",
                    path,
                    line_number(text, match.start()),
                    "long-duration",
                    f"Duration `{match.group(0)}` exceeds the 300ms UI budget. Keep only if this is marketing, modal, drawer, or explained motion.",
                )
            )

    if path.suffix != ".html" and has_motion and not has_reduced_motion:
        findings.append(
            Finding(
                "MEDIUM",
                path,
                1,
                "missing-reduced-motion",
                "File contains motion but no visible reduced-motion branch.",
            )
        )

    if has_hover_motion and not has_pointer_gate:
        findings.append(
            Finding(
                "MEDIUM",
                path,
                1,
                "ungated-hover-motion",
                "Hover motion should be gated with `@media (hover: hover) and (pointer: fine)`.",
            )
        )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit common motion craft failures.")
    parser.add_argument("paths", nargs="+", type=Path, help="Files or directories to scan")
    parser.add_argument("--max-findings", type=int, default=200, help="Stop printing after this many findings")
    args = parser.parse_args()

    files = iter_files(args.paths)
    findings: list[Finding] = []
    for file_path in files:
        findings.extend(audit_file(file_path))

    if not findings:
        print(f"Motion audit passed: scanned {len(files)} files.")
        return 0

    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    findings.sort(key=lambda item: (order.get(item.severity, 9), str(item.path), item.line, item.rule))

    print(f"Motion audit found {len(findings)} finding(s) across {len(files)} file(s):")
    for finding in findings[: args.max_findings]:
        print(f"{finding.severity} {finding.path}:{finding.line} [{finding.rule}] {finding.message}")

    if len(findings) > args.max_findings:
        print(f"... {len(findings) - args.max_findings} more finding(s) hidden by --max-findings.")

    return 1 if any(item.severity == "HIGH" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
