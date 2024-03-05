import asyncio
import os

import aiohttp

from ExcelReader import ExcelReader
from ExcelExporter import ExcelExporter
from DataProcessor import DataProcessor
from WebsiteFetcher import WebsiteFetcher
from RowResult import RowResult


async def main():
    # input_file_path = "..\\xlSplitted\\s_ח-ל.xlsx"
    # input_file_path = "..\\xl\\hebBigShort.xlsx"
    # input_file_path = "..\\xlSplitted\\s_מ-ת.xlsx"
    # input_file_path = "..\\xlSplitted\\s_א-ל.xlsx"
    input_file_path = "..\\xlSplitted\\s_z.xlsx"

    output_file_path = os.path.splitext(input_file_path)[0] + "Output.xlsx"
    original_column = 'original'  # 'Trns'
    only_is_dotted = False

    undoubted = ExcelReader(input_file_path, original_column)
    undoubted.read_sheets()

    if undoubted.dataframes is not None:
        processor = DataProcessor(undoubted.dataframes)
        processor.remove_unnecessary_characters()

        async with aiohttp.ClientSession() as session:
            hebrew_academy_fetcher = WebsiteFetcher()
            row_results = await fetch_and_process_data(processor, original_column, hebrew_academy_fetcher, session)

        processor.row_results = row_results
        processor.fill_values_from_html(only_is_dotted=only_is_dotted)
        processor.add_idioms_sheet()
        exporter = ExcelExporter(processor.dataframes, output_file_path)
        exporter.export_to_excel()


async def fetch_and_process_data(processor, original_column, hebrew_academy_fetcher, session):
    tasks = []
    try:
        for sheet_name, df in processor.dataframes.items():

            for index, row in df.iterrows():
                word = row[original_column]
                try:
                    task = asyncio.create_task(hebrew_academy_fetcher.fetch(session, word))
                    tasks.append(task)
                except aiohttp.ClientError as e:
                    tasks.append(None)
                    print(f"An error occurred while processing word {word}: {e}")
    except Exception as e:
        raise Exception("An error occurred while fetching and processing data:", e)

    results = [await task if task is not None else RowResult() for task in tasks]
    return results

if __name__ == "__main__":
    asyncio.run(main())
