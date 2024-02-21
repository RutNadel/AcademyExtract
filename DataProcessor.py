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
                        val = val.split(' (')[0].strip()

                        val = val.replace('!', '').strip()

                        if '/' in val:
                            val = val.split('/')[0].strip()

                        df.at[i, col] = val
        self._dataframes = self._dataframes
