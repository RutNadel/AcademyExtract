import unittest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from urllib.parse import quote
import subprocess
import re
from curl import get_html_response, extract_rellevant_fields_and_print, filter_list


class TestHebrewFunctions(unittest.TestCase):

    def test_filter_list(self):
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
        filtered_words = filter_list(words)
        self.assertEqual(filtered_words, ["אוֹפֶּרָה", "אוֹקְטָבָה", "אוֹרְגָן", "אָקוֹרְד", "אָקוֹרְדְּיוֹן", "אָבוֹקָדוֹ", "אֶגְרוֹל"])

    @patch('subprocess.Popen')
    @patch('bs4.BeautifulSoup')
    def test_get_html_response(self, mock_soup, mock_popen):
        expected_soup = Mock()
        mock_soup.return_value = expected_soup
        mock_popen.return_value.communicate.return_value = (b'<html>Mock HTML</html>', None)
        result = get_html_response('אוֹפֶּרָה')
        self.assertEqual(result, expected_soup)

    @patch('builtins.print')
    def test_extract_rellevant_fields_and_print(self, mock_print):
        mock_soup = Mock()
        mock_soup.find_all.return_value = ['אוֹפֶּרָה', 'משה', 'אברהם']
        extract_rellevant_fields_and_print(mock_soup, 'אוֹפֶּרָה')
        mock_print.assert_called_once_with('אוֹפֶּרָה * משה * אברהם')


if __name__ == '__main__':
    unittest.main()
