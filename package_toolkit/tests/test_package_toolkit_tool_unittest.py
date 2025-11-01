import unittest
import os
import zipfile
from pathlib import Path
import shutil
import tempfile
from package_toolkit.package_toolkit_tool import main, OUTPUT_ZIP, OUTPUT_DIR, PROJECT_ROOT

def create_dummy_tool(name, with_readme=True):
    tool_dir = PROJECT_ROOT / name
    tool_dir.mkdir(exist_ok=True)
    (tool_dir / 'tool.py').write_text('# Dummy tool\n')
    if with_readme:
        (tool_dir / 'README.md').write_text('# Dummy Tool\n\n## Purpose\nA dummy tool for testing.\n')
    return tool_dir

def remove_dummy_tool(name):
    tool_dir = PROJECT_ROOT / name
    if tool_dir.exists():
        shutil.rmtree(tool_dir)

class TestPackageToolkit(unittest.TestCase):
    def setUp(self):
        self.dummy_tools = ['toolA', 'toolB']
        for name in self.dummy_tools:
            create_dummy_tool(name)
        # Ensure output dir exists
        OUTPUT_DIR.mkdir(exist_ok=True)
        # Remove old zip if exists
        if OUTPUT_ZIP.exists():
            OUTPUT_ZIP.unlink()
        # Remove old summary README if exists
        summary_readme = PROJECT_ROOT / 'SUMMARY_README.md'
        if summary_readme.exists():
            summary_readme.unlink()

    def tearDown(self):
        for name in self.dummy_tools:
            remove_dummy_tool(name)
        # Remove output zip
        if OUTPUT_ZIP.exists():
            OUTPUT_ZIP.unlink()
        # Remove summary README
        summary_readme = PROJECT_ROOT / 'SUMMARY_README.md'
        if summary_readme.exists():
            summary_readme.unlink()

    def test_package_toolkit_creates_zip_and_readme(self):
        main()
        self.assertTrue(OUTPUT_ZIP.exists())
        # Check zip contents
        with zipfile.ZipFile(OUTPUT_ZIP, 'r') as zipf:
            namelist = zipf.namelist()
            self.assertIn('COMBINED_README.md', namelist)
            self.assertIn('toolA/tool.py', namelist)
            self.assertIn('toolB/tool.py', namelist)
        # Check summary README was removed after packaging
        summary_readme = PROJECT_ROOT / 'SUMMARY_README.md'
        self.assertFalse(summary_readme.exists())

    def test_readme_only(self):
        import sys
        sys.argv = ['package_toolkit_tool.py', '--readme-only']
        main()
        summary_readme = PROJECT_ROOT / 'SUMMARY_README.md'
        self.assertTrue(summary_readme.exists())
        # Check contents
        content = summary_readme.read_text()
        self.assertIn('Dummy Tool', content)
        self.assertIn('A dummy tool for testing.', content)
        summary_readme.unlink()

if __name__ == '__main__':
    unittest.main()
