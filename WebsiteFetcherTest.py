import asyncio
import pandas as pd
from WebsiteFetcher import WebsiteFetcher


async def main():
    hebrew_academy_fetcher = WebsiteFetcher()
    df = pd.DataFrame({'original': ['אַרְנָק', 'אָמָּן/אָמָּנִית', 'אוֹקְטָבָה', 'אֶגְרוֹל']})
    await hebrew_academy_fetcher.fetch(df)
    print(df)

if __name__ == "__main__":
    asyncio.run(main())


import asyncio
import unittest
from unittest.mock import AsyncMock, Mock, patch
from WebsiteFetcher import WebsiteFetcher

class TestWebsiteFetcher(unittest.IsolatedAsyncioTestCase):
    async def test_fetch_tidy_with_valid_word(self):
        # Arrange
        mock_session = AsyncMock()
        mock_session.get.return_value.__aenter__.return_value.status = 200
        mock_session.get.return_value.__aenter__.return_value.text = asyncio.coroutine(lambda: '<html><body>Hello</body></html>')()

        fetcher = WebsiteFetcher()
        word = 'example'

        # Act
        result = await fetcher._fetch_tidy(mock_session, word)

        # Assert
        self.assertEqual(result.success, True)
        self.assertEqual(result.word, word)
        self.assertEqual(result.idioms, [])
        self.assertEqual(result.tables, [])

    async def test_fetch_tidy_with_empty_word(self):
        # Arrange
        fetcher = WebsiteFetcher()
        word = ''

        # Act
        result = await fetcher._fetch_tidy(Mock(), word)

        # Assert
        self.assertEqual(result.success, False)
        self.assertEqual(result.error, 'the word is empyt')
        self.assertEqual(result.word, word)
        self.assertIsNone(result.tables)
        self.assertIsNone(result.idioms)

    async def test_fetch_tidy_with_404_response(self):
        # Arrange
        mock_session = AsyncMock()
        mock_session.get.return_value.__aenter__.return_value.status = 404

        fetcher = WebsiteFetcher()
        word = 'example'

        # Act
        result = await fetcher._fetch_tidy(mock_session, word)

        # Assert
        self.assertEqual(result.success, False)
        self.assertEqual(result.word, word)
        self.assertIsNone(result.tables)
        self.assertIsNone(result.idioms)

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
