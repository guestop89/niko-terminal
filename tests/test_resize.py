import importlib.util
from pathlib import Path
import re
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('niko', Path(__file__).resolve().parents[1] / 'niko.py')
niko = importlib.util.module_from_spec(spec)
spec.loader.exec_module(niko)

class ResizeTests(unittest.TestCase):
    def test_fits_terminal_without_changing_proportions(self):
        for columns, lines in [(90, 40), (40, 24), (20, 15), (80, 12), (3, 7), (1, 1)]:
            with self.subTest(columns=columns, lines=lines):
                with patch.object(niko.shutil, 'get_terminal_size', return_value=(columns, lines)):
                    grid = niko.grid_for_terminal()
                    self.assertTrue(not grid or len(grid) == len(grid[0]))
                    rows = re.sub(r'\x1b\[[0-9;]*m', '', niko.render()).splitlines()
                    self.assertLessEqual(len(rows), max(0, lines - 5))
                    self.assertTrue(all(len(row) < columns for row in rows))

    def test_restores_original_detail_when_terminal_grows(self):
        with patch.object(niko.shutil, 'get_terminal_size', return_value=(90, 40)):
            self.assertEqual(niko.grid_for_terminal(), niko.PIXELS)

if __name__ == '__main__':
    unittest.main()
