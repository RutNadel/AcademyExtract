from urllib.parse import quote
from bs4 import BeautifulSoup
import re


class HebrewAcademyFetcher:
    def __init__(self, basic_url='https://hebrew-academy.org.il/keyword/'):
        self._basic_url = basic_url

    async def fetch_html_response(self, session, word):
        try:
            if isinstance(word, str):
                url = self._basic_url + quote(word, encoding='utf-8')
            else:
                return False, None, "the word is empyt", None

            async with session.get(url) as response:
                if response.status == 404:
                    #print(f" False | 404 - Page miss for word: {word}")
                    return False, None, word, None
                elif response.status in range(200, 300):
                    html = await response.text()
                    word_full_details = HebrewAcademyFetcher.extract_and_process(html, word)
                    word_info = word_full_details[0]
                    word_tserfuim = word_full_details[1]
                    #print(f" True | 200+ Page found for word: {word}")
                    return True, word_info, word, word_tserfuim
        except Exception as e:
            print(word, e)
            return False, None, word, None

    async def fetch_and_process_word(self, session, word):
        is_found = await self.fetch_html_response(session, word)
        if is_found is None:
            return False, None, word, None
        print(word, end=" ")
        return is_found

    @staticmethod
    def extract_and_process(html, word):
        """
        extract specific values from the html (like tables or links or lists)
        :param html:
        :return: list of all extracted values.
        the first value in 0th index is: list of tables values (into dictionaries). the second is : צירופים
        """
        soup = BeautifulSoup(html, 'html.parser')
        tables_list = []

        tables = soup.find_all('table')

        if not tables:
            return tables_list

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


        #
        if word == "יָד":
            print('h')

        # list_items = soup.find_all('ul', class_='tserufim more')
        list_items = soup.find_all('ul', class_=['tserufim', 'tserufim more'])

        # Extract the Hebrew text from each list of items
        hebrew_texts = []
        for ul in list_items:
            items = ul.find_all('a')
            for item in items:
                text = item.text.strip()  # Remove leading and trailing whitespace
                # Use regular expression to extract Hebrew text
                hebrew_text = re.findall(r'[\u0590-\u05FF\s]+', text)
                if hebrew_text:
                    hebrew_texts.append(hebrew_text[0].strip())

        # Print the extracted Hebrew text
        for text in hebrew_texts:
            print(text)

        html_values = [tables_list, hebrew_texts]
        return html_values
