import os
import subprocess
import json
import tempfile
import unittest

SCRIPT = os.path.abspath("skills/tastemaker/scripts/check_contrast.py")

class TestCheckContrast(unittest.TestCase):
    def test_single_pair_text(self):
        res = subprocess.run(["python3", SCRIPT, "050315", "fbfbfe"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("[PASS] given pair:", res.stdout)

    def test_single_pair_json(self):
        res = subprocess.run(["python3", SCRIPT, "--json", "050315", "fbfbfe"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data["mode"], "pair")
        self.assertTrue(data["passed"])
        self.assertGreaterEqual(data["pair"]["ratio"], 4.5)
        self.assertEqual(data["pair"]["classification"], "text-safe")

    def test_palette_json(self):
        res = subprocess.run(["python3", SCRIPT, "--json", "--palette", "text=050315", "bg=fbfbfe", "primary=2f27ce"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data["mode"], "palette")
        self.assertTrue(data["passed"])
        self.assertEqual(len(data["checks"]), 4)

    def test_matrix_json(self):
        res = subprocess.run(["python3", SCRIPT, "--json", "--matrix", "text=e6e6ea", "bg=0b0d12", "primary=047857"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data["mode"], "matrix")
        self.assertIn("legal_pairings", data)
        self.assertIn("text_safe", data["legal_pairings"])
        self.assertIn("ui_safe", data["legal_pairings"])

    def test_check_lock_pass(self):
        lock_content = """# Style lock
## Palette
- Background: #fbfbfe
- Text primary: #050315
- Primary: #2f27ce
- Surface: #ffffff
## Color contract
- Text-safe (>=4.5): text/bg, text/surface
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
            f.write(lock_content)
            temp_path = f.name
        
        try:
            res = subprocess.run(["python3", SCRIPT, "--check-lock", temp_path], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)
            self.assertIn("[PASS] All contrast checks", res.stdout)
        finally:
            os.remove(temp_path)

    def test_check_lock_fail_regression(self):
        lock_content = """# Style lock
## Palette
- Background: #888888
- Text primary: #777777
- Primary: #2f27ce
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
            f.write(lock_content)
            temp_path = f.name
        
        try:
            res = subprocess.run(["python3", SCRIPT, "--check-lock", temp_path], capture_output=True, text=True)
            self.assertEqual(res.returncode, 1)
            self.assertIn("[FAIL] Contrast regressions found", res.stderr)
        finally:
            os.remove(temp_path)

if __name__ == "__main__":
    unittest.main()
