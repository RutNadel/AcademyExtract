import pandas as pd
import asyncio
from bs4 import BeautifulSoup
import aiohttp
from urllib.parse import quote


class HebrewAcademyFetcher:
    def __init__(self, basic_url='https://hebrew-academy.org.il/keyword/'):
        self._basic_url = basic_url
        self._soup = None

    async def fetch_html_response(self, word):
        if ' ' in word:
            print(f"Word '{word}' contains more than one word. Skipping fetch. צרוף")
            return False
        url = self._basic_url + quote(word, encoding='utf-8')

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 404:
                    print(f"404 - Page not found for word: {word}")
                    return False
                elif response.status in range(200, 300):
                    html = await response.text()
                    self._soup = BeautifulSoup(html, 'html.parser')
                    return True

    async def process_html_response(self, word):
        is_found = await self.fetch_html_response(word)
        return is_found

    # async def fetch_and_process_words(self, df):
    #     results = []
    #     for word in df['original']:
    #         is_found = await self.process_html_response(word)
    #         results.append(is_found)
    #     df['isDotted'] = results
    async def fetch_and_process_words(self, df):
        for index, row in df.iterrows():
            word = row['original']
            is_found = await self.fetch_html_response(word)
            df.at[index, 'isDotted'] = is_found




