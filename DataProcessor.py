import re
from collections import namedtuple

import pandas as pd

Config = namedtuple('Config', ['value'])
default = Config(value="-")


class DataProcessor:
    def __init__(self, dataframes):
        self._dataframes = dataframes
        self._idioms = []
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
        for sheet_name, df in self.dataframes.items():
            is_dotted_col = self._columns.get("isDotted", None)
            if is_dotted_col is None:
                continue  # Skip this sheet if isDotted column is not found

            columns_to_assign = ["isDotted", "pos", "root", "gender", "pl"]

            # Assign default values to specified columns
            for column_name in columns_to_assign:
                df[column_name] = default.value

            num_rows = len(df)

            for row in range(num_rows):
                # Ensure we don't exceed the length of _results
                if row >= len(self._results):
                    break

                missing_value = False  # Default value if data is missing

                is_found_index = 0
                word_info_index = 1
                word_idioms_index = 3

                try:
                    is_data_for_word = self._results[row][is_found_index]
                    if is_data_for_word is None or is_data_for_word == 'nan':
                        df.iloc[row, is_dotted_col] = missing_value
                    else:
                        df.iloc[row, is_dotted_col] = bool(is_data_for_word)

                        if not only_is_dotted:
                            word_info = self._results[row][word_info_index]
                            idioms_info = self._results[row][word_idioms_index]

                            self._fill_data(sheet_name, word_info, row)
                            self.find_idioms(sheet_name, idioms_info, row)

                except IndexError:
                    print("Error: Index out of range while updating dataframe")
                except Exception as e:
                    print(f"Error occurred while updating dataframe at row {row}:", e)


        # def update_dataframe(self, only_is_dotted=True):
    #     index = -1
    #     for sheet_name, df in self.dataframes.items():
    #         isDotted = self._columns.get("isDotted")
    #
    #         columns_to_assign = ["isDotted", "pos", "root", "gender", "pl"]
    #
    #         for column_name in columns_to_assign:
    #             self.dataframes[sheet_name][column_name] = default.value
    #
    #         num_rows = len(df)
    #
    #         for row in range(num_rows):
    #
    #             if index < len(self._results):
    #                 index += 1
    #
    #                 missing_value = False  # if proxy blocked
    #
    #                 is_found_index = 0
    #                 word_info_index = 1
    #                 word_index = 2
    #                 word_idioms_index = 3
    #
    #                 try:
    #                     is_data_for_word = self._results[index][is_found_index]
    #                     if is_data_for_word is None:
    #                         self.dataframes[sheet_name].iloc[row, isDotted] = missing_value
    #                     elif is_data_for_word == 'nan':
    #                         self.dataframes[sheet_name].iloc[row, isDotted] = missing_value
    #                     elif is_data_for_word is False:
    #                         self.dataframes[sheet_name].iloc[row, isDotted] = is_data_for_word
    #                     elif is_data_for_word is True:
    #                         self.dataframes[sheet_name].iloc[row, isDotted] = True
    #                         if not only_is_dotted:
    #                             word_info = self._results[index][word_info_index]
    #                             idioms_info = self._results[index][word_idioms_index]
    #
    #                             self._fill_data(sheet_name, word_info, row)
    #                             self.find_idioms(sheet_name, idioms_info, row)
    #
    #                 except Exception as e:
    #                     print("Error occurred while updating dataframe:", e)
    
    def _fill_data(self, sheet_name, word_info, row):
        try:
            columns_names = ["original", "isDotted", "pos", "root", "gender", "pl"]
            original, isDotted, pos, root, gender, pl = (
                self._columns.get(column_name) for column_name in columns_names
            )
            if word_info and len(word_info) > 0:  # sometimes few table
                first_table = 0
                pl_value = word_info[first_table].get('נטייה', default.value)
                clean_pl_value = pl_value.replace("לכל הנטיות", "")

                building_value = word_info[first_table].get('בניין', default.value)
                gender_value = word_info[first_table].get('מין', default.value)
                pos_value = word_info[first_table].get('חלק דיבר', default.value)
                if pos_value == default.value:
                    if gender_value != default.value:  # כאשר יש מין זה שם עצם
                        pos_value = 'שם עצם'
                    elif building_value:  # כאשר יש בנין זה פועל
                        pos_value = 'פועל'

                self.dataframes[sheet_name].iloc[row, pos] = pos_value
                self.dataframes[sheet_name].iloc[row, root] = word_info[first_table].get('שורש', default.value)
                self.dataframes[sheet_name].iloc[row, gender] = gender_value
                self.dataframes[sheet_name].iloc[row, pl] = clean_pl_value

                self.dataframes[sheet_name].iloc[row, isDotted] = True
        except Exception as e:
            print(f"Error occurred while filling dataframe: {e}")

    def find_idioms(self, sheet_name, idioms_info, row):
        try:
            if idioms_info and len(idioms_info) > 0:  # sometimes few table
                self._idioms.append(idioms_info)
        except Exception as e:
            print(f"Error occurred while filling idioms: {e}")

    def add_idioms_sheet(self):
        flattened_idioms = [item for sublist in self._idioms for item in sublist]
        idioms_df = pd.DataFrame({'full_idioms': flattened_idioms})

        self.dataframes["idioms"] = idioms_df

