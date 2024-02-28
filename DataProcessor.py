import numpy as np
import pandas as pd
import re


class DataProcessor:
    def __init__(self, dataframes):
        self._dataframes = dataframes
        self._results = None
        self._columns = {
            "original": 0,
            "isDotted": 1,
            "pos": 2,
            "root": 3,
            "gender": 4,
            "pl": 5
        }

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
                        # cleaned_val = cleaned_val.replace('-', '').strip()
                        if '/' in cleaned_val:
                            cleaned_val = cleaned_val.split('/')[0].strip()

                        df.at[i, col] = cleaned_val

        self._dataframes = self._dataframes

    def update_dataframe(self, only_is_dotted=True):
        try:
            index = -1
            for sheet_name, df in self.dataframes.items():
                isDotted = self._columns.get("isDotted")

                columns_to_assign = ["isDotted", "pos", "root", "gender", "pl"]
                default_value = "-"
                for column_name in columns_to_assign:
                    self.dataframes[sheet_name][column_name] = default_value

                num_rows = len(df)

                for row in range(num_rows):

                    if index < len(self._results):
                        index += 1

                        missing_value = False  # if proxy blocked

                        is_found_index = 0
                        word_info_index = 1
                        word_index = 2

                        try:
                            is_data_for_word = self._results[index][is_found_index]
                            if is_data_for_word is None:
                                self.dataframes[sheet_name].iloc[row, isDotted] = missing_value
                            elif is_data_for_word == 'nan':
                                self.dataframes[sheet_name].iloc[row, isDotted] = missing_value
                            elif is_data_for_word is False:
                                self.dataframes[sheet_name].iloc[row, isDotted] = is_data_for_word
                            elif is_data_for_word is True:
                                self.dataframes[sheet_name].iloc[row, isDotted] = True
                                if not only_is_dotted:
                                    word_info = self._results[index][word_info_index]

                                    self._fill_data(sheet_name, word_info, row)

                        except Exception as e:
                            print("Error occurred while updating dataframe:", e)
        except Exception as e:
            print("An error occurred while updating dataframe:", e)

    def _fill_data(self, sheet_name, word_info, row):
        try:
            columns_names = ["original", "isDotted", "pos", "root", "gender", "pl"]
            original, isDotted, pos, root, gender, pl = (
                self._columns.get(column_name) for column_name in columns_names
            )
            if len(word_info) > 0:  # sometimes few table
                first_table = 0
                pl_value = word_info[first_table].get('נטייה', '-')
                clean_pl_value = pl_value.replace("לכל הנטיות", "")

                building_value = word_info[first_table].get('בניין', '-')
                gender_value = word_info[first_table].get('מין', '-')
                pos_value = word_info[first_table].get('חלק דיבר', '-')
                if pos_value == '-':
                    if gender_value:
                        pos_value = 'שם עצם'
                    elif building_value:
                        pos_value = 'פועל'

                self.dataframes[sheet_name].iloc[row, pos] = pos_value
                self.dataframes[sheet_name].iloc[row, root] = word_info[first_table].get('שורש', '-')
                self.dataframes[sheet_name].iloc[row, gender] = gender_value
                self.dataframes[sheet_name].iloc[row, pl] = clean_pl_value

                self.dataframes[sheet_name].iloc[row, isDotted] = True
        except Exception as e:
            print(f"Error occurred while filling dataframe: {e}")

