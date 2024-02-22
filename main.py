import asyncio
import aiohttp

from ExcelReader import ExcelReader
from ExcelExporter import ExcelExporter
from DataProcessor import DataProcessor
from HebrewAcademyFetcher import HebrewAcademyFetcher


async def fetch_and_process_data(processor, hebrew_academy_fetcher, session):
    tasks = []
    try:
        for sheet_name, df in processor.dataframes.items():
            for index, row in df.iterrows():
                word = row['original']
                task = asyncio.create_task(hebrew_academy_fetcher.fetch_and_process_word(session, word, df))
                tasks.append(task)
    except Exception as e:
        print("An error occurred while fetching and processing data:", e)
    return await asyncio.gather(*tasks)


def update_dataframe(processor, results):
    try:
        index = -1
        for sheet_name, df in processor.dataframes.items():
            processor.dataframes[sheet_name]["isDotted"] = True
            num_rows = len(df)
            for i in range(num_rows):
                if index < len(results):
                    index += 1
                    try:
                        processor.dataframes[sheet_name].iloc[i, 1] = results[index]
                    except Exception as e:
                        print("Error occurred while updating dataframe:", e)
    except Exception as e:
        print("An error occurred while updating dataframe:", e)


async def main():
    try:
        unpoint_reader = ExcelReader("..\\heb_dictEnd.xlsx")
        unpoint_reader.read_sheets()

        if unpoint_reader.dataframes is not None:
            processor = DataProcessor(unpoint_reader.dataframes)
            processor.remove_unnecessary_characters()

            async with aiohttp.ClientSession() as session:
                hebrew_academy_fetcher = HebrewAcademyFetcher()
                results = await fetch_and_process_data(processor, hebrew_academy_fetcher, session)

            update_dataframe(processor, results)

            excel_path = '..\\excel_dottedEnd.xlsx'
            exporter = ExcelExporter(processor.dataframes, excel_path)
            exporter.export_to_excel()
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    asyncio.run(main())
