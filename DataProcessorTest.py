import unittest
import pandas as pd
from DataProcessor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    def test_remove_parentheses(self):
        data = {'col1': ['שלום', 'אהבה', 'דעת', 'שלום!', 'אהבה / רצון', 'דעת ()']}
        df = pd.DataFrame(data)

        expected_result = {'col1': ['שלום', 'אהבה', 'דעת', 'שלום', 'אהבה', 'דעת']}
        expected_df = pd.DataFrame(expected_result)

        processor = DataProcessor({'Sheet1': df})
        processor._remove_parentheses()

        self.assertTrue(df.equals(expected_df))


if __name__ == '__main__':
    unittest.main()
