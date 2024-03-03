import pandas as pd


class ExcelReader:
    def __init__(self, file_path, column_name):
        self._file_path = file_path
        self._dataframes = None
        self._column_name = column_name

    @property
    def dataframes(self):
        return self._dataframes

    def read_sheets(self):
        try:
            xl = pd.ExcelFile(self._file_path)
            self._dataframes = {}
            for sheet_name in xl.sheet_names:
                df = xl.parse(sheet_name)
                if self._column_name in df.columns:
                    self._dataframes[sheet_name] = df[[self._column_name]]
                else:
                    print(f"No '{self._column_name}' column found in sheet '{sheet_name}'. Skipping...")
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self._file_path}' not found.")
        except Exception as e:
            raise IOError(f"An error occurred while reading the file: {e}")
