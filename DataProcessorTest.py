import unittest
import pandas as pd
from DataProcessor import DataProcessor
#

class TestDataProcessor(unittest.TestCase):
    def test_remove_parentheses(self):
        # Create a sample DataFrame
        data = {'col1': ['שלום', 'אהבה', 'דעת', 'שלום!', 'אהבה / רצון', 'דעת ()']}
        # data = {'col1': ['hello (world)', 'bye ! ', 'ruth \ rachel', 'ruth \dsf \ dfsf']}
        df = pd.DataFrame(data)

        # Expected result after removing parentheses, exclamation marks, and backslashes
        expected_result = {'col1': ['שלום', 'אהבה', 'דעת', 'שלום', 'אהבה', 'דעת']}
        expected_df = pd.DataFrame(expected_result)

        # Create an instance of DataProcessor and call the _remove_parentheses method
        processor = DataProcessor({'Sheet1': df})
        processor._remove_parentheses()

        # Check if the result matches the expected DataFrame
        self.assertTrue(df.equals(expected_df))


if __name__ == '__main__':
    unittest.main()
