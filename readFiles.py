import pandas as pd


class ExcelReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_sheet(self, sheet_name, column_name='original'):
        try:
            # Read the specified sheet from the Excel file
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            if column_name in df.columns:
                return df[column_name]
            else:
                print(f"Column '{column_name}' not found in sheet '{sheet_name}'.")
                return None
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None

# Example usage:
if __name__ == "__main__":
    # Create an instance of ExcelReader with the file path
    excel_reader = ExcelReader("your_file.xlsx")

    # Read a specific sheet
    sheet_name = "Sheet1"
    column_name = "original"
    sheet_data = excel_reader.read_sheet(sheet_name, column_name)

    if sheet_data is not None:
        print(f"Data from sheet '{sheet_name}', column '{column_name}':")
        print(sheet_data)
