import re
class DataProcessor:
    def __init__(self, dataframes):
        self._dataframes = dataframes

    @property
    def dataframes(self):
        return self._dataframes

    def remove_unnecessary_characters(self):
        self._remove_parentheses()

    def _remove_parentheses(self):
        for sheet_name, df in self._dataframes.items():
            for col in df.columns:
                for i, val in enumerate(df[col]):
                    if isinstance(val, str):
                        # df.at[i, col] = val.split(' (')[0].strip()
                        # Remove content inside parentheses
                        val = val.split(' (')[0].strip()

                        # Remove '!' and trailing whitespace
                        val = val.replace('!', '').strip()

                        # Remove '\' and everything after it
                        if '/' in val:
                            val = val.split('/')[0].strip()

                        df.at[i, col] = val
        self._dataframes = self._dataframes

    def is_properly_punctuated(self, text):
        return True

    def add_properly_punctuated_column(self):
        for sheet_name, df in self._dataframes.items():
            properly_punctuated_column = df.apply(lambda x: self.is_properly_punctuated(x['original']), axis=1)
            self._dataframes[sheet_name] = df.assign(properlyPunctuated=properly_punctuated_column)

