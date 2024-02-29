from urllib.parse import quote
from bs4 import BeautifulSoup


class HebrewAcademyFetcher:
    def __init__(self, basic_url='https://hebrew-academy.org.il/keyword/'):
        self._basic_url = basic_url

    async def fetch_html_response(self, session, word):
        try:
            if isinstance(word, str):
                url = self._basic_url + quote(word, encoding='utf-8')
            else:
                return False, None, "the word is empyt"

            async with session.get(url) as response:
                if response.status == 404:
                    #print(f" False | 404 - Page miss for word: {word}")
                    return False, None, word
                elif response.status in range(200, 300):
                    html = await response.text()
                    word_info = HebrewAcademyFetcher.extract_and_process(html)
                    #print(f" True | 200+ Page found for word: {word}")
                    return True, word_info, word
        except Exception as e:
            print(word, e)
            return False, None, word

    async def fetch_and_process_word(self, session, word):
        is_found = await self.fetch_html_response(session, word)
        if is_found is None:
            return False, None, word
        print(word, end=" ")
        return is_found

    @staticmethod
    def extract_and_process(html):
        soup = BeautifulSoup(html, 'html.parser')
        extracted_info_list = []

        tables = soup.find_all('table')

        if not tables:
            return extracted_info_list

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
            extracted_info_list.append(extracted_info)

        return extracted_info_list
