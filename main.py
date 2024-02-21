import pandas as pd
import pandas as pd
import asyncio
from bs4 import BeautifulSoup
import aiohttp
from urllib.parse import quote
from ExcelReader import ExcelReader
from ExcelExporter import ExcelExporter
from DataProcessor import DataProcessor
from HebrewAcademyFetcher import HebrewAcademyFetcher
async def main():
    unpoint_reader = ExcelReader("heb_dict.xlsx")
    unpoint_reader.read_sheets()

    if unpoint_reader.dataframes is not None:
        processor = DataProcessor(unpoint_reader.dataframes)
        processor.remove_unnecessary_characters()

        hebrew_academy_fetcher = HebrewAcademyFetcher()
        tasks = []

        async with aiohttp.ClientSession() as session:
            for sheet_name, df in processor.dataframes.items():
                for index, row in df.iterrows():
                    word = row['original']
                    task = asyncio.create_task(hebrew_academy_fetcher.fetch_and_process_word(session, word))
                    tasks.append(task)

            await asyncio.gather(*tasks)

        excel_path = 'excel_dotted.xlsx'
        exporter = ExcelExporter(processor.dataframes, excel_path)
        exporter.export_to_excel()


if __name__ == "__main__":
    asyncio.run(main())





# #semaphore
# import asyncio
# from ExcelReader import ExcelReader
# from ExcelExporter import ExcelExporter
# from DataProcessor import DataProcessor
# from HebrewAcademyFetcher import HebrewAcademyFetcher
#
#
# async def main():
#     unpoint_reader = ExcelReader("heb_dict.xlsx")
#     unpoint_reader.read_sheets()
#
#     if unpoint_reader.dataframes is not None:
#         processor = DataProcessor(unpoint_reader.dataframes)
#         processor.remove_unnecessary_characters()
#
#         hebrew_academy_fetcher = HebrewAcademyFetcher()
#         tasks = []
#
#         total_requests = sum(len(df) for df in processor.dataframes.values())
#         completed_requests = [0]  # Mutable list to hold the value of completed requests
#
#         semaphore = asyncio.Semaphore(200)  # Adjust the semaphore limit as needed
#
#         for sheet_name, df in processor.dataframes.items():
#             for index, row in df.iterrows():
#                 word = row['original']
#                 task = asyncio.create_task(hebrew_academy_fetcher.fetch_and_process_word(word, semaphore, total_requests, completed_requests))
#                 tasks.append(task)
#             break
#
#         for task in asyncio.as_completed(tasks):
#             await task
#
#         excel_path = 'excel_dotted.xlsx'
#         exporter = ExcelExporter(processor.dataframes, excel_path)
#         exporter.export_to_excel()
#
#
# if __name__ == "__main__":
#     asyncio.run(main())


