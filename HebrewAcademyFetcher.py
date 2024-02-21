import pandas as pd
import asyncio
from bs4 import BeautifulSoup
import aiohttp
from urllib.parse import quote
from ExcelReader import ExcelReader
from ExcelExporter import ExcelExporter
from DataProcessor import DataProcessor


class HebrewAcademyFetcher:
    def __init__(self, basic_url='https://hebrew-academy.org.il/keyword/'):
        self._basic_url = basic_url

    async def fetch_html_response(self, session, word):
        try:
            if ' ' in word:
                print(f"Word '{word}' contains more than one word. Skipping fetch. צרוף")
                return False
            url = self._basic_url + quote(word, encoding='utf-8')

            async with session.get(url) as response:
                if response.status == 404:
                    print(f"404 - Page not found for word: {word}")
                    return False
                elif response.status in range(200, 300):
                    html = await response.text()
                    print("found")
                    return True
        except TypeError:
            print(word)

    async def fetch_and_process_word(self, session, word):
        is_found = await self.fetch_html_response(session, word)
        return is_found
# #semaphore
# import aiohttp
# from urllib.parse import quote
# from bs4 import BeautifulSoup
# import asyncio
#
#
# class HebrewAcademyFetcher:
#     def __init__(self, basic_url='https://hebrew-academy.org.il/keyword/'):
#         self._basic_url = basic_url
#         self._soup = None
#
#     async def fetch_html_response(self, word):
#         try:
#             if ' ' in word:
#                 print(f"Word '{word}' contains more than one word. Skipping fetch. צרוף")
#                 return False
#             url = self._basic_url + quote(word, encoding='utf-8')
#
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(url) as response:
#                     if response.status == 404:
#                         print(f"404 - Page not found for word: {word}")
#                         return False
#                     elif response.status in range(200, 300):
#                         html = await response.text()
#                         self._soup = BeautifulSoup(html, 'html.parser')
#                         print("found")
#                         return True
#         except TypeError:
#             print(word)
#
#     async def fetch_and_process_word(self, word, semaphore, total_requests, completed_requests):
#         async with semaphore:
#             is_found = await self.fetch_html_response(word)
#             completed_requests[0] += 1
#             print(f"{completed_requests[0]}/{total_requests}")
#             return is_found
#
