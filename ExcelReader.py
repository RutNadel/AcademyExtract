import pandas as pd


class ExcelReader:
    def __init__(self, file_path):
        self._file_path = file_path
        self._dataframes = None

    @property
    def dataframes(self):
        return self._dataframes

    def read_sheets(self, column_name='original'):
        try:
            xl = pd.ExcelFile(self._file_path)
            self._dataframes = {}
            for sheet_name in xl.sheet_names:
                df = xl.parse(sheet_name)
                if column_name in df.columns:
                    self._dataframes[sheet_name] = df[[column_name]]
                else:
                    print(f"No '{column_name}' column found in sheet '{sheet_name}'. Skipping...")
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

