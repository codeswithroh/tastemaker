#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path

from install_cursor import find_skill_root, install, rewrite_paths


class TestInstallCursor(unittest.TestCase):
    def test_rewrite_paths(self):
        sample = "Run scripts/check_contrast.py or check references/palette.md"
        rewritten = rewrite_paths(sample)
        self.assertIn(".tastemaker/skill/scripts/check_contrast.py", rewritten)
        self.assertIn(".tastemaker/skill/references/palette.md", rewritten)

    def test_install_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            skill_root = find_skill_root(Path(__file__).parent)
            install(tmp_path, skill_root)

            mdc_path = tmp_path / ".cursor" / "rules" / "tastemaker.mdc"
            self.assertTrue(mdc_path.is_file())
            content = mdc_path.read_text(encoding="utf-8")
            self.assertIn("---", content)
            self.assertIn(".tastemaker/skill/scripts/", content)

            for d in ("references", "scripts"):
                self.assertTrue((tmp_path / ".tastemaker" / "skill" / d).is_dir())


if __name__ == "__main__":
    unittest.main()
