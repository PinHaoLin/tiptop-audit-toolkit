import os
import sys
import types
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import openpyxl  # noqa: F401
except ModuleNotFoundError:
    sys.modules['openpyxl'] = types.ModuleType('openpyxl')

import core_logic


class CoreLogicMatchingTests(unittest.TestCase):
    def test_exact_file_name_matches_excel_program_code(self):
        self.assertTrue(core_logic.is_file_matching_excel('azzi910', 'azzi910'))

    def test_localized_suffix_matches_base_program_code(self):
        self.assertTrue(core_logic.is_file_matching_excel('azzi910_tw', 'azzi910'))
        self.assertTrue(core_logic.is_file_matching_excel('azzi910', 'azzi910_std'))

    def test_different_program_code_does_not_match(self):
        self.assertFalse(core_logic.is_file_matching_excel('azzi910', 'azzi920'))

    def test_empty_values_do_not_match(self):
        self.assertFalse(core_logic.is_file_matching_excel('', 'azzi910'))
        self.assertFalse(core_logic.is_file_matching_excel('azzi910', ''))


if __name__ == '__main__':
    unittest.main()
