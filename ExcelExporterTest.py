import unittest
import pandas as pd
import os
from ExcelExporter import ExcelExporter


class TestExcelExporter(unittest.TestCase):
    def setUp(self):
        # Sample dataframes for testing
        self.dataframes = {
            'Sheet1': pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}),
            'Sheet2': pd.DataFrame({'C': [7, 8, 9], 'D': [10, 11, 12]})
        }
        self.excel_path = 'test_output.xlsx'
        self.exporter = ExcelExporter(self.dataframes, self.excel_path)

    def tearDown(self):
        # Delete the test output file
        import os
        if os.path.exists(self.excel_path):
            os.remove(self.excel_path)

    def test_dataframes_property(self):
        self.assertEqual(self.exporter.dataframes, self.dataframes)

    def test_excel_path_property(self):
        self.assertEqual(self.exporter.excel_path, self.excel_path)

    def test_dataframes_setter(self):
        new_dataframes = {'NewSheet': pd.DataFrame({'X': [1, 2, 3]})}
        self.exporter.dataframes = new_dataframes
        self.assertEqual(self.exporter.dataframes, new_dataframes)

    def test_excel_path_setter(self):
        new_excel_path = 'new_test_output.xlsx'
        self.exporter.excel_path = new_excel_path
        self.assertEqual(self.exporter.excel_path, new_excel_path)

    def test_export_to_excel(self):
        # Export to Excel
        self.exporter.export_to_excel()
        # Check if the file is created
        self.assertTrue(os.path.exists(self.excel_path))


if __name__ == '__main__':
    unittest.main()
