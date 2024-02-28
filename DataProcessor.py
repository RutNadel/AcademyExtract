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

                        cleaned_val = cleaned_val.split(' (')[0].strip()
                        cleaned_val = cleaned_val.replace('!', '').strip()
                        cleaned_val = cleaned_val.replace('?', '').strip()
                        cleaned_val = cleaned_val.replace('-', '').strip()
                        if '/' in cleaned_val:
                            cleaned_val = cleaned_val.split('/')[0].strip()

                        df.at[i, col] = cleaned_val

        self._dataframes = self._dataframes

    def update_dataframe(self, only_is_dotted=True):

        try:
            index = -1
            for sheet_name, df in self.dataframes.items():

                self.dataframes[sheet_name]["pos"] = "-"
                self.dataframes[sheet_name]["root"] = "-"
                self.dataframes[sheet_name]["gender"] = "-"
                self.dataframes[sheet_name]["pl"] = "-"
                self.dataframes[sheet_name]["isDotted"] = True

                original = 0
                pos = 1
                root = 2
                gender = 3
                pl = 4
                isDotted = 5

                num_rows = len(df)

                for i in range(num_rows):

                    if index < len(self._results):
                        index += 1

                        missing_value = False  # if proxy blocked

                        is_found_index = 0
                        word_info_index = 1
                        word_index = 2

                        try:
                            is_data_for_word = self._results[index][is_found_index]
                            if is_data_for_word is None:
                                self.dataframes[sheet_name].iloc[i, isDotted] = missing_value
                            elif is_data_for_word == 'nan':
                                self.dataframes[sheet_name].iloc[i, isDotted] = missing_value
                            elif is_data_for_word is False:
                                self.dataframes[sheet_name].iloc[i, isDotted] = is_data_for_word
                            elif is_data_for_word is True:

                                # fill data
                                word_info = self._results[index][word_info_index]

                                pl_value = word_info[0].get('נטייה', '-')
                                clean_pl_value = pl_value.replace("לכל הנטיות", "")

                                building_value = word_info[0].get('בניין', '-')
                                gender_value = word_info[0].get('מין', '-')
                                pos_value = word_info[0].get('חלק דיבר', '-')
                                if pos_value == '-':
                                    if gender_value:
                                        pos_value = 'שם עצם'
                                    elif building_value:
                                        pos_value = 'פועל'

                                self.dataframes[sheet_name].iloc[i, pos] = pos_value
                                self.dataframes[sheet_name].iloc[i, root] = word_info[0].get('שורש', '-')
                                self.dataframes[sheet_name].iloc[i, gender] = gender_value
                                self.dataframes[sheet_name].iloc[i, pl] = clean_pl_value
                                #'נטיית הפועל'
                                self.dataframes[sheet_name].iloc[i, isDotted] = True

                        except Exception as e:
                            print("Error occurred while updating dataframe:", e)
        except Exception as e:
            print("An error occurred while updating dataframe:", e)


