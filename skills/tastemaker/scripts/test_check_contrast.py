#!/usr/bin/env python3
"""Tests for check_contrast.py --json / --lock / --from-lock.

Run: python3 test_check_contrast.py
Stdlib only. Exits nonzero on the first failure.
"""

import json
import os
import subprocess
import sys
import tempfile

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_contrast.py")


def run(*args):
    return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)


def check(cond, msg):
    if not cond:
        print(f"FAIL: {msg}")
        sys.exit(1)
    print(f"ok: {msg}")


def write_lock(tmp, palette_lines, contract_lines):
    path = os.path.join(tmp, "style-lock.md")
    with open(path, "w") as f:
        f.write("# Style lock — test\n\n## Palette\n" + palette_lines
                + "\n## Color contract\n\n" + contract_lines)
    return path


def main():
    # pair --json
    p = run("--json", "050315", "fbfbfe")
    check(p.returncode == 0, "pair json exit 0")
    d = json.loads(p.stdout)
    check(d["mode"] == "pair" and d["pass"] is True and d["checks"][0]["ratio"] > 4.5,
          "pair json shape + pass")
    p2 = run("--json", "050315", "fbfbfe")
    check(p.stdout == p2.stdout, "pair json deterministic")
    p = run("--json", "777777", "888888")
    check(p.returncode == 1 and json.loads(p.stdout)["pass"] is False,
          "pair json failing pair exits 1")

    # palette --json
    p = run("--palette", "--json", "text=050315", "bg=fbfbfe", "primary=2f27ce",
            "secondary=dedcff", "accent=433bff")
    check(p.returncode == 0, "palette json exit 0")
    d = json.loads(p.stdout)
    check(d["mode"] == "palette" and d["pass"] is True and len(d["checks"]) == 5,
          "palette json has 5 checks and passes")

    # matrix --json
    p = run("--matrix", "--json", "text=e6e6ea", "bg=0b0d12", "surface=161a21",
            "primary=047857", "accent=34d399", "border=232a33", "on-primary=ffffff")
    check(p.returncode == 0, "matrix json exit 0")
    d = json.loads(p.stdout)
    check(d["mode"] == "matrix" and len(d["pairs"]) == 21, "matrix json has 21 pairs")
    check(all(set(x) >= {"color1", "color2", "ratio", "class"} for x in d["pairs"]),
          "matrix pair objects carry ratio + class")
    check(set(d["legal_pairings"]) == {"text_safe", "ui_safe", "decorative"},
          "matrix legal pairings grouped")
    check(d["pairs"] == sorted(d["pairs"], key=lambda x: -x["ratio"]),
          "matrix pairs sorted by ratio desc")

    # matrix text header unchanged
    p = run("--matrix", "text=e6e6ea", "bg=0b0d12")
    check("== Contrast matrix (2 roles, 1 pairs) ==" in p.stdout, "matrix text header")

    # style-lock gate on synthetic locks
    with tempfile.TemporaryDirectory() as tmp:
        bad = write_lock(tmp, "- Background: #ffffff\n- Text primary: #fefefe\n",
                         "- Text-safe (>=4.5): bg/text (21.0)\n")
        p = run("--from-lock", bad)
        check(p.returncode == 1 and "FAIL bg/text" in p.stdout,
              "gate fails and names the offending pair")
        p = run("--from-lock", "--json", bad)
        d = json.loads(p.stdout)
        check(d["gate"]["pass"] is False and d["gate"]["offenders"][0]["pair"] == "bg/text",
              "gate json names the offender")
        good = write_lock(tmp, "- Background: #ffffff\n- Text primary: #000000\n",
                          "- Text-safe (>=4.5): bg/text (21.0)\n")
        p = run("--from-lock", good)
        check(p.returncode == 0 and "OK: all 1 recorded" in p.stdout,
              "gate passes on a good lock")
        p = run("--matrix", "--lock", bad, "bg=ffffff", "text=fefefe")
        check(p.returncode == 1 and "FAIL bg/text" in p.stdout,
              "matrix --lock fails and names the offender")
        p = run("--matrix", "--lock", good, "bg=ffffff", "text=000000")
        check(p.returncode == 0, "matrix --lock passes on a good lock")

    # the repo's real style lock must pass its own gate
    repo_lock = os.path.normpath(os.path.join(os.path.dirname(SCRIPT),
                                               "..", "..", "..",
                                               ".tastemaker", "style-lock.md"))
    if os.path.exists(repo_lock):
        p = run("--from-lock", repo_lock)
        check(p.returncode == 0, "real style lock passes its own gate")

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
