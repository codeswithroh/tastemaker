"""Contract tests for the command-line contrast checker."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/tastemaker/scripts/check_contrast.py"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True)


class ContrastCliTests(unittest.TestCase):
    def test_pair_and_palette_json_status(self):
        pair = run("--json", "ffffff", "000000")
        self.assertEqual(pair.returncode, 0)
        self.assertEqual(json.loads(pair.stdout)["pairs"][0]["class"], "text-safe")
        palette = run("--palette", "text=ffffff", "bg=ffffff", "--json")
        self.assertEqual(palette.returncode, 1)
        self.assertFalse(json.loads(palette.stdout)["passed"])

    def test_matrix_has_all_pairs_and_groups(self):
        result = run("--matrix", "a=ffffff", "b=000000", "c=eeeeee", "--json")
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(len(data["pairs"]), 3)
        self.assertIn("a/b", data["legal_pairings"]["text-safe"])
        self.assertIn("a/c", data["legal_pairings"]["decorative"])

    def test_lock_regression_names_pair_and_fails_action(self):
        with tempfile.TemporaryDirectory() as directory:
            lock = Path(directory) / "style-lock.md"
            lock.write_text("# Style lock\n\n## Palette\n- Background: #ffffff\n"
                            "- Text primary: #000000\n- Primary: #111111\n"
                            "- Button label color: white\n\n## Color contract\n"
                            "Legal pairings:\n- Text-safe (>=4.5): text/bg, on-primary/primary\n"
                            "- UI-safe (>=3.0): none\n", encoding="utf-8")
            passing = run("--check-lock", str(lock), "--json")
            self.assertEqual(passing.returncode, 0, passing.stderr)
            lock.write_text(lock.read_text().replace("#000000", "#eeeeee"))
            failing = run("--check-lock", str(lock), "--json")
            self.assertEqual(failing.returncode, 1)
            self.assertIn("text/bg", failing.stderr)
            self.assertFalse(json.loads(failing.stdout)["passed"])

    def test_invalid_lock_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            lock = Path(directory) / "style-lock.md"
            lock.write_text("## Palette\n- Background: #ffffff\n")
            result = run("--check-lock", str(lock))
            self.assertEqual(result.returncode, 1)
            self.assertIn("Color contract", result.stderr)


if __name__ == "__main__":
    unittest.main()
