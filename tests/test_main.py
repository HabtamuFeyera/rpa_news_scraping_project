# Unit tests for main.py
import sys
sys.path.append('/home/habte/rpa_news_scraping_project/src')

import unittest
from unittest.mock import patch
from src.main import main


class TestMain(unittest.TestCase):
    @patch('main.NewsScraper')
    def test_main_functionality(self, MockNewsScraper):
        # Mock environment variables
        with patch.dict('os.environ', {'SEARCH_PHRASE': 'Python', 'NEWS_CATEGORY': 'Technology', 'NUM_MONTHS': '1', 'EXCEL_FILE_PATH': 'output.xlsx'}):
            # Mock NewsScraper instance
            mock_scraper = MockNewsScraper.return_value
            mock_scraper.scrape_headlines.return_value = [{'title': 'Python is awesome', 'link': '/article/1'}, {'title': 'Python 2.0 released', 'link': '/article/2'}]
            mock_scraper.scrape_news_details.side_effect = [('Python is awesome', '2022-04-13', 'Python is an interpreted, high-level and general-purpose programming language.', 'image1.jpg'), ('Python 2.0 released', '2022-04-12', 'Python 2.0 brings many new features and improvements.', 'image2.jpg')]

            # Call main function
            main()

            # Assert expected behavior
            # For example, you can assert that the NewsScraper methods were called with the correct arguments
            mock_scraper.scrape_headlines.assert_called_once_with('Python', 'Technology', 1)
            mock_scraper.scrape_news_details.assert_any_call('https://www.example.com/article/1')
            mock_scraper.scrape_news_details.assert_any_call('https://www.example.com/article/2')
            mock_scraper.save_to_excel.assert_called_once()
            mock_scraper.driver.quit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
