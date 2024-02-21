import pandas as pd

class ExcelExporter:
    def __init__(self, dataframes, excel_path):
        self._dataframes = dataframes
        self._excel_path = excel_path

    @property
    def dataframes(self):
        return self._dataframes

    @dataframes.setter
    def dataframes(self, value):
        self._dataframes = value

    @property
    def excel_path(self):
        return self._excel_path

    @excel_path.setter
    def excel_path(self, value):
        self._excel_path = value

    def export_to_excel(self):
        with pd.ExcelWriter(self._excel_path) as writer:
            for sheet_name, df in self._dataframes.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
