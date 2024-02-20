from ExcelReader import ExcelReader
from DataProcessor import DataProcessor


def main():
    unpoint_reader = ExcelReader("heb_dict.xlsx")
    unpoint_reader.read_sheets()
    if unpoint_reader.dataframes is not None:
        processor = DataProcessor(unpoint_reader.dataframes)

        processor.remove_parentheses()

        processor.add_properly_punctuated_column()

        # Display the processed DataFrames
        for sheet_name, df in processor._dataframes.items():
            print(f"Processed data from sheet '{sheet_name}':")
            print(df)


if __name__ == "__main__":
    main()