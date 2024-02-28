import asyncio
import os

import aiohttp

from ExcelReader import ExcelReader
from ExcelExporter import ExcelExporter
from DataProcessor import DataProcessor
from HebrewAcademyFetcher import HebrewAcademyFetcher


async def main():
    input_file_path = "..\\xlSplitted\\H_א-ל.xlsx"
    output_file_path = os.path.splitext(input_file_path)[0] + "Output.xlsx"
    original_column = 'original'  # 'Trns'
    only_is_dotted = False

    try:
        undoubted = ExcelReader(input_file_path, original_column)
        undoubted.read_sheets()

        if undoubted.dataframes is not None:
            processor = DataProcessor(undoubted.dataframes)
            processor.remove_unnecessary_characters()

            async with aiohttp.ClientSession() as session:
                hebrew_academy_fetcher = HebrewAcademyFetcher()
                results = await fetch_and_process_data(processor, original_column, hebrew_academy_fetcher, session)

            processor.results = results
            processor.update_dataframe(only_is_dotted=only_is_dotted)

            exporter = ExcelExporter(processor.dataframes, output_file_path)
            exporter.export_to_excel()

    except Exception as e:
        print("An error occurred while main process:", e)


async def fetch_and_process_data(processor, original_column, hebrew_academy_fetcher, session):
    tasks = []
    try:
        for sheet_name, df in processor.dataframes.items():
            for index, row in df.iterrows():
                word = row[original_column]
                task = asyncio.create_task(hebrew_academy_fetcher.fetch_and_process_word(session, word))
                tasks.append(task)
    except Exception as e:
        print("An error occurred while fetching and processing data:", e)
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
