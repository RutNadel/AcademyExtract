import pandas as pd


def create_output_file(output_prefix, sheet_names, xl):
    output_file = f"{output_prefix}_{sheet_names[0]}-{sheet_names[-1]}.xlsx"
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

    for sheet_name in sheet_names:
        df = xl.parse(sheet_name)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    writer.close()


def split_excel_file(input_file, output_prefix, max_rows_per_file):
    xl = pd.ExcelFile(input_file)
    sheet_names = xl.sheet_names

    total_rows_per_sheet = {sheet_name: xl.parse(sheet_name).shape[0] for sheet_name in sheet_names}

    current_rows = 0
    current_sheets = []

    for sheet_name, rows in total_rows_per_sheet.items():

        if current_rows + rows <= max_rows_per_file:
            current_rows += rows
            current_sheets.append(sheet_name)
        else:
            create_output_file(output_prefix, current_sheets, xl)
            current_sheets = [sheet_name]
            current_rows = rows

    if current_sheets:
        create_output_file(output_prefix, current_sheets, xl)


if __name__ == "__main__":
    input_file = '..\\engHeb.xlsx'
    output_prefix = '..\\H'
    max_rows_per_file = 10000

    split_excel_file(input_file, output_prefix, max_rows_per_file)
