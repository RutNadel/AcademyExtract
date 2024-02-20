import asyncio
import pandas as pd
from HebrewAcademyFetcher import HebrewAcademyFetcher


async def main():
    hebrew_academy_fetcher = HebrewAcademyFetcher()
    df = pd.DataFrame({'original': ['אַרְנָק', 'אָמָּן/אָמָּנִית', 'אוֹקְטָבָה', 'אֶגְרוֹל']})
    await hebrew_academy_fetcher.fetch_and_process_words(df)
    print(df)

if __name__ == "__main__":
    asyncio.run(main())
