"""Regression tests against Tastemaker's shipped style-lock palette."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/tastemaker/scripts/check_contrast.py"
LOCK = ROOT / ".tastemaker/style-lock.md"


def check_lock(path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--check-lock", str(path), "--json"],
        text=True, capture_output=True,
    )


class ShippedStyleLockTests(unittest.TestCase):
    def test_declared_text_safe_pairs_remain_legal(self):
        result = check_lock(LOCK)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual(payload["mode"], "matrix")
        declared = LOCK.read_text(encoding="utf-8").split(
            "- Text-safe (>=4.5): ", 1
        )[1].splitlines()[0]
        self.assertEqual(len(declared.split(", ")), 15)

    def test_primary_colour_regression_fails_with_pair_name(self):
        original = LOCK.read_text(encoding="utf-8")
        self.assertIn("- Primary: #008286", original)
        with tempfile.TemporaryDirectory() as directory:
            changed = Path(directory) / "style-lock.md"
            changed.write_text(
                original.replace("- Primary: #008286", "- Primary: #FFFFFF", 1),
                encoding="utf-8",
            )
            result = check_lock(changed)
        self.assertEqual(result.returncode, 1)
        self.assertIn("primary/on-primary", result.stderr)
        self.assertFalse(json.loads(result.stdout)["passed"])


if __name__ == "__main__":
    unittest.main()
