import asyncio
import aiohttp

from ExcelReader import ExcelReader
from ExcelExporter import ExcelExporter
from DataProcessor import DataProcessor
from HebrewAcademyFetcher import HebrewAcademyFetcher


async def fetch_and_process_data(processor, hebrew_academy_fetcher, session):
    tasks = []
    for sheet_name, df in processor.dataframes.items():
        for index, row in df.iterrows():
            word = row['original']
            task = asyncio.create_task(hebrew_academy_fetcher.fetch_and_process_word(session, word, df))
            tasks.append(task)
    return await asyncio.gather(*tasks)


def update_dataframe(processor, results):
    index = -1
    for sheet_name, df in processor.dataframes.items():
        processor.dataframes[sheet_name]["b"] = True
        num_rows = len(df)
        for i in range(num_rows):
            if index < len(results):
                index += 1
                try:
                    processor.dataframes[sheet_name].iloc[i, 1] = results[index]
                except Exception as e:
                    print("Error occurred:", e)

async def main():
    unpoint_reader = ExcelReader("..\\heb_dict.xlsx")
    unpoint_reader.read_sheets()

    if unpoint_reader.dataframes is not None:
        processor = DataProcessor(unpoint_reader.dataframes)
        processor.remove_unnecessary_characters()

        # async with aiohttp.ClientSession() as session:
        #     hebrew_academy_fetcher = HebrewAcademyFetcher()
        #     results = await fetch_and_process_data(processor, hebrew_academy_fetcher, session)
        #
        # update_dataframe(processor, results)

        excel_path = '..\\excel_dotted.xlsx'
        exporter = ExcelExporter(processor.dataframes, excel_path)
        exporter.export_to_excel()

if __name__ == "__main__":
    asyncio.run(main())


