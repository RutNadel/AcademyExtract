import unittest
import pandas as pd
from DataProcessor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        # Create sample DataFrames
        self.df1 = pd.DataFrame({'original': ['ruth (ddd)', 'b (dsf sdf)', ' b b b (d)', 'b   ']})
        self.df2 = pd.DataFrame({'original': ['test1 (text)', 'test2 (more text)']})
        self.dataframes = {'Sheet1': self.df1, 'Sheet2': self.df2}
        self.processor = DataProcessor(self.dataframes)

    def test_remove_parentheses(self):
        # Call the remove_parentheses method
        self.processor.remove_parentheses()

        # Check if parentheses are removed from the DataFrame cells
        expected_df1 = pd.DataFrame({'original': ['ruth', 'b', 'b b b', 'b']})
        expected_df2 = pd.DataFrame({'original': ['test1', 'test2']})
        self.assertTrue(self.processor._dataframes['Sheet1'].equals(expected_df1))
        self.assertTrue(self.processor._dataframes['Sheet2'].equals(expected_df2))


if __name__ == '__main__':
    unittest.main()
