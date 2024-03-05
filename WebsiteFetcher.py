from urllib.parse import quote
from itertools import chain
import aiohttp
from bs4 import BeautifulSoup
import re
from RowResult import RowResult


class WebsiteFetcher:
    def __init__(self, basic_url='https://hebrew-academy.org.il/keyword/'):
        self._basic_url = basic_url

    async def fetch_tidy(self, session, word):
        try:
            if isinstance(word, str):
                url = self._basic_url + quote(word, encoding='utf-8')
            else:
                return RowResult(False, "the word is empyt", word, None)

            async with session.get(url) as response:
                if response.status == 404:
                    return RowResult(False, None, word, None)
                elif response.status in range(200, 300):
                    html = await response.text()
                    row_result = WebsiteFetcher.extract_from_html(html, word)
                    return row_result

        except aiohttp.client_exceptions.ClientOSError as e:
            raise Exception(f"the io http failed: {e}")
        except TimeoutError as e:
            raise TimeoutError("Timeout occurred while fetching data") from e
        except Exception as e:
            print(f"Error occured while fetch html response with the word: {word} got the error messange: {e}")
            return RowResult(False, None, word, None)

    async def fetch(self, session, word):
        row_result = await self.fetch_tidy(session, word)
        if row_result is None:
            return RowResult(False, None, word, None)
        print('`', end="")
        # print(word, end=" . ")
        return row_result

    @staticmethod
    def extract_idoms(soup):
        try:
            base_tserufim = soup.find_all('ul', class_='tserufim')
            more_tseroufim = soup.find_all('ul', class_='tserufim more')
            all_tserufim = chain(base_tserufim, more_tseroufim)

            idioms = []
            for ul in all_tserufim:
                items = ul.find_all('a')
                for item in items:
                    text = item.text.strip()
                    hebrew_text = re.findall(r'[\u0590-\u05FF\s]+', text)
                    if hebrew_text:
                        idioms.append(hebrew_text[0].strip())
            return idioms
        except Exception as e:
            print(f"error while extract idoms for soup: {soup} with error: {e}")
            return []

    @staticmethod
    def extract_tables(soup):
        try:
            tables_list = []
            tables = soup.find_all('table')

            if not tables:
                return []
            else:
                for table in tables:
                    extracted_info = {}
                    rows = table.find_all('tr')
                    for row in rows:
                        header = row.find('th')
                        data = row.find('td')
                        if header and data:
                            key = header.get_text(strip=True)
                            value = data.get_text(strip=True)
                            extracted_info[key] = value
                    tables_list.append(extracted_info)
            return tables_list
        except Exception as e:
            print(f"error while extract table for soup: {soup}, with error: {e}")
            return []

    @staticmethod
    def extract_from_html(html, word):
        """
        extract specific values from the html (like tables or links or lists)
        :param html:
        :return: list of all extracted values.
        the first value in 0th index is: list of tables values (into dictionaries). the second is : צירופים
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            tables = WebsiteFetcher.extract_tables(soup)
            idioms = WebsiteFetcher.extract_idoms(soup)
            row_result = RowResult(True, tables, word, idioms)
            return row_result
        except Exception as e:
            raise e
            # return RowResult(True, [], word, [])
