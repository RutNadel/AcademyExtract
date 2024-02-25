import unittest
import pandas as pd
from DataProcessor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    def test_remove_parentheses(self):
        data = {'col1': ['שלום', 'אהבה', 'דעת', 'שלום!', 'אהבה / רצון', 'דעת ()', 123, None, '',
                         " word1 / word2 / word3 ", "word", " word ", "  word  ", "word ", "word!",
                         "word?", "word-", "word1 (word2)", "word1 (word2 (word3))", "word1 / word2",
                         " word1 / word2 "]}
        df = pd.DataFrame(data)

        expected_result = {'col1': ['שלום', 'אהבה', 'דעת', 'שלום', 'אהבה', 'דעת', 123, None, '', "word1",
                                    "word", "word", "word", "word", "word", "word", "word", "word1", "word1", "word1",
                                    "word1"]}
        expected_df = pd.DataFrame(expected_result)

        processor = DataProcessor({'Sheet1': df})
        processor.remove_unnecessary_characters()

        self.assertTrue(df.equals(expected_df))


if __name__ == '__main__':
    unittest.main()
