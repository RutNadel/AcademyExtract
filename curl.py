from bs4 import BeautifulSoup
from urllib.parse import quote
import subprocess
import re


def filter_list(words=None):

    if words is None:
        words = [
            "אַרְנָק (לְכֶסֶף קָטָן)",
            "אַרְנָק (לִשְׁטָרוֹת)",
            "אוֹפֶּרָה",
            "אוֹקְטָבָה",
            "אוֹרְגָן",
            "אָקוֹרְד (בְּמוּזִיקָה)",
            "אָקוֹרְדְּיוֹן",
            "אָבוֹקָדוֹ",
            "אֶגְרוֹל",
            "אוֹזְנֵי הָמָן"
        ]
    pattern = re.compile(r'\s*\(.*?\)')
    filtered_words = [pattern.sub('', word) for word in words] # delete ()
    for word in filtered_words[:]:    # delete 2 words
        if ' ' in word:
            filtered_words.remove(word)
    return filtered_words


def get_html_response(word, basic_url='https://hebrew-academy.org.il/keyword/'):
    word = quote(word, encoding='utf-8')
    curl_get = 'curl -X GET '
    curl_command = ''.join([curl_get, basic_url, word])
    process = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    soup = BeautifulSoup(stdout.decode(), 'html.parser')
    return soup


def extract_rellevant_fields_and_print(soup, word):
    try:
        hebrew_text = [element.get_text() for element in soup.find_all(string=True) if
                       any(char > '\u0590' and char < '\u05ff' for char in element)]
        index_first = hebrew_text.index(word)
        index_second = hebrew_text.index(word, index_first + 1)
        sublist = hebrew_text[index_second: index_second + 20]

        filtered_list = sublist
        elements_per_line = 5

        for i in range(0, len(filtered_list), elements_per_line):
            line = ' * '.join(filtered_list[i:i + elements_per_line])
            print(line)
    except ValueError:
        print(f"The value wasn't found for the {word}")

def main():
    filtered_words = filter_list()
    for word in filtered_words:
        # word = filtered_words[0]
        soup = get_html_response(word)
        extract_rellevant_fields_and_print(soup, word)


main()
