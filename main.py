from ExcelReader import ExcelReader
from ExcelExported import ExcelExporter
from DataProcessor import DataProcessor
from HebrewAcademyFetcher import HebrewAcademyFetcher
import asyncio


async def main():
    unpoint_reader = ExcelReader("heb_dict.xlsx")
    unpoint_reader.read_sheets()

    if unpoint_reader.dataframes is not None:
        processor = DataProcessor(unpoint_reader.dataframes)
        processor.remove_unnecessary_characters()

        # processor.add_properly_punctuated_column()#delete this function pls
        hebrew_academy_fetcher = HebrewAcademyFetcher()
        tasks = []
        count = 0
        for sheet_name, df in processor.dataframes.items():
            count += 1
            if count == 6:
                print(f"Processing data from sheet '{sheet_name}':")
                task = asyncio.create_task(hebrew_academy_fetcher.fetch_and_process_words(df))
                tasks.append(task)

        await asyncio.gather(*tasks)

        excel_path = 'excel_dotted.xlsx'
        exporter = ExcelExporter(processor.dataframes, excel_path)
        exporter.export_to_excel()
        # for sheet_name, df in processor._dataframes.items(): #print all sheets
        #     print(df)


if __name__ == "__main__":
    asyncio.run(main())
