from urllib.parse import quote

import aiohttp
from aiohttp import ClientOSError
from bs4 import BeautifulSoup
import re
from RowResult import RowResult


class HebrewAcademyFetcher:
    def __init__(self, basic_url='https://hebrew-academy.org.il/keyword/'):
        self._basic_url = basic_url

    async def fetch_html_response(self, session, word):
        try:

            if isinstance(word, str):
                url = self._basic_url + quote(word, encoding='utf-8')
            else:
                return RowResult(False, "the word is empyt", word, None)

            async with session.get(url) as response:
                if response.status == 404:
                    #print(f" False | 404 - Page miss for word: {word}")
                    return RowResult(False, None, word, None)
                elif response.status in range(200, 300):
                    html = await response.text()
                    row_result = HebrewAcademyFetcher.extract_and_process(html, word)
                    #print(f" True | 200+ Page found for word: {word}")
                    return row_result

        except aiohttp.client_exceptions.ClientOSError as e:
            raise Exception(f"the io http failed: {e}")
        except TimeoutError as e:
            raise TimeoutError("Timeout occurred while fetching data") from e
        except Exception as e:
            print(f"Error occured while fetch html response with the word: {word} got the error messange: {e}")
            return RowResult(False, None, word, None)


    async def fetch_and_process_word(self, session, word):
        row_result = await self.fetch_html_response(session, word)
        if row_result is None:
            return RowResult(False, None, word, None)

        print(word, end=" . ")
        return row_result

    @staticmethod
    def extract_and_process(html, word):
        """
        extract specific values from the html (like tables or links or lists)
        :param html:
        :return: list of all extracted values.
        the first value in 0th index is: list of tables values (into dictionaries). the second is : צירופים
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            tables_list = []

            tables = soup.find_all('table')

            if not tables:
                tables_list=[]
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

            # list_items = soup.find_all('ul', class_=['tserufim', 'tserufim more'])
            try:
                list_items = soup.find_all('ul', class_=['tserufim', 'tserufim more'])
            except AttributeError:
                # Handle the case where no elements with the specified classes are found
                print("Could not find elements with the specified classes. Trying to find with only one class...")
                try:
                    # Try finding elements with only one class
                    list_items = soup.find_all('ul', class_='tserufim')
                except AttributeError:
                    print("Could not find elements with only one class as well.")

            idioms = []
            for ul in list_items:
                items = ul.find_all('a')
                for item in items:
                    text = item.text.strip()
                    # Use regular expression to extract Hebrew text
                    hebrew_text = re.findall(r'[\u0590-\u05FF\s]+', text)
                    if hebrew_text:
                        idioms.append(hebrew_text[0].strip())
            row_result = RowResult(True, tables_list, word, idioms)

            return row_result

        except Exception as e:
            raise(e)
            # return RowResult(True, [], word, [])
