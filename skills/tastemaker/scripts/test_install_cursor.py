import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from install_cursor import install, make_rule


class CursorInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.project = self.root / "project with spaces"
        for directory in ("scripts", "references", "assets", "ideagram/scripts"):
            (self.source / directory).mkdir(parents=True, exist_ok=True)
        (self.source / "SKILL.md").write_text(
            '---\nname: test\ndescription: Design UI: with scripts\n---\n'
            '`references/style.md` `scripts/generate_palette.py` '
            '`ideagram/scripts/tool.py` `.tastemaker/style-lock.md`\n', encoding="utf-8")
        (self.source / "references/style.md").write_text("reference", encoding="utf-8")
        (self.source / "assets/sample.bin").write_bytes(b"\x00\xff")
        (self.source / "ideagram/scripts/tool.py").write_text("print('ok')", encoding="utf-8")
        for name in ("generate_palette.py", "check_contrast.py"):
            shutil.copy2(Path(__file__).parent / name, self.source / "scripts" / name)

    def test_install_preserves_resources_and_runs_real_helpers(self):
        rule = install(self.source, self.project)
        content = rule.read_text(encoding="utf-8")
        self.assertIn('description: "Design UI: with scripts"', content)
        self.assertIn(".tastemaker/skill/references/style.md", content)
        self.assertIn(".tastemaker/skill/ideagram/scripts/tool.py", content)
        self.assertNotIn("ideagram/.tastemaker", content)
        self.assertIn("`.tastemaker/style-lock.md`", content)
        installed = self.project / ".tastemaker/skill"
        self.assertEqual((installed / "assets/sample.bin").read_bytes(), b"\x00\xff")
        for name, args in (
            ("generate_palette.py", ["--mood", "technical", "--seed", "7"]),
            ("check_contrast.py", ["--matrix", "text=000000", "bg=ffffff"]),
        ):
            result = subprocess.run([sys.executable, str(installed / "scripts" / name), *args],
                                    cwd=self.project, capture_output=True, text=True,
                                    encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(result.stdout.strip())

    def test_repeat_and_upgrade_preserve_project_memory(self):
        rule = install(self.source, self.project)
        first = rule.read_bytes()
        memory = self.project / ".tastemaker/style-lock.md"
        memory.write_text("user choices", encoding="utf-8")
        install(self.source, self.project)
        self.assertEqual(first, rule.read_bytes())
        (self.source / "references/style.md").write_text("updated", encoding="utf-8")
        install(self.source, self.project)
        self.assertEqual((self.project / ".tastemaker/skill/references/style.md").read_text(), "updated")
        self.assertEqual(memory.read_text(), "user choices")

    def test_refuses_unmanaged_rule_before_copy(self):
        rule = self.project / ".cursor/rules/tastemaker.mdc"
        rule.parent.mkdir(parents=True)
        rule.write_text("custom rule", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "not installer-managed"):
            install(self.source, self.project)
        self.assertEqual(rule.read_text(), "custom rule")
        self.assertFalse((self.project / ".tastemaker").exists())

    def test_refuses_overlap(self):
        with self.assertRaisesRegex(ValueError, "overlap"):
            install(self.source, self.source)

    def test_requires_frontmatter(self):
        with self.assertRaises(ValueError):
            make_rule("no frontmatter")


if __name__ == "__main__":
    unittest.main()
