from urllib.parse import quote


class HebrewAcademyFetcher:
    def __init__(self, basic_url='https://hebrew-academy.org.il/keyword/'):
        self._basic_url = basic_url

    async def fetch_html_response(self, session, word):
        try:
            # if ' ' in word:
            #     print(f"Word '{word}' contains more than one word. Skipping fetch. צרוף")
            #     return False

            url = self._basic_url + quote(word, encoding='utf-8')

            async with session.get(url) as response:
                if response.status == 404:
                    print(f" False | 404 - Page miss for word: {word}")
                    return False
                elif response.status in range(200, 300):
                    html = await response.text()
                    print(f" True | 200+ Page found for word: {word}")
                    return True
        except Exception as e:
            print(word, e)
            return False

    async def fetch_and_process_word(self, session, word, df):
        is_found = await self.fetch_html_response(session, word)
        return is_found

