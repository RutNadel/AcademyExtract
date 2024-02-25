import numpy as np
import pandas as pd
import re
class DataProcessor:
    def __init__(self, dataframes):
        self._dataframes = dataframes
        self._results = None

    @property
    def dataframes(self):
        return self._dataframes

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, results):
        assert isinstance(results, list)
        self._results = results

    def remove_unnecessary_characters(self):

        for sheet_name, df in self._dataframes.items():
            for col in df.columns:
                for i, val in enumerate(df[col]):
                    if isinstance(val, str):
                        words = re.split(r'\s+', val.strip())
                        cleaned_words = [word.strip() for word in words]
                        cleaned_val = ' '.join(cleaned_words)

                        # Additional cleaning
                        cleaned_val = cleaned_val.split(' (')[0].strip()
                        cleaned_val = cleaned_val.replace('!', '').strip()
                        cleaned_val = cleaned_val.replace('?', '').strip()
                        cleaned_val = cleaned_val.replace('-', '').strip()
                        if '/' in cleaned_val:
                            cleaned_val = cleaned_val.split('/')[0].strip()

                        df.at[i, col] = cleaned_val
                    #     val = val.split(' (')[0].strip()
                    #
                    #     val = val.replace('!', '').strip()
                    #     val = val.replace('?', '').strip()
                    #     val = val.replace('-', '').strip()
                    #
                    #     if '/' in val:
                    #         val = val.split('/')[0].strip()
                    #
                    #     df.at[i, col] = val
        self._dataframes = self._dataframes

    def update_dataframe(self):
        try:
            index = -1
            for sheet_name, df in self.dataframes.items():
                self.dataframes[sheet_name]["isDotted"] = True
                num_rows = len(df)
                for i in range(num_rows):
                    if index < len(self._results):
                        index += 1
                        missing_value = False # if netfree blocked
                        try:
                            if self._results[index] is None:
                                self.dataframes[sheet_name].iloc[i, 1] = missing_value
                            elif self._results[index] == 'nan':
                                self.dataframes[sheet_name].iloc[i, 1] = missing_value
                            else:
                                self.dataframes[sheet_name].iloc[i, 1] = bool(self._results[index])
                        except Exception as e:
                            print("Error occurred while updating dataframe:", e)
        except Exception as e:
            print("An error occurred while updating dataframe:", e)


