# Unit tests for news_scraper.py
import sys
sys.path.append('/home/habte/rpa_news_scraping_project/src/')

import unittest
from unittest.mock import patch
from src.news_scraper import NewsScraper

class TestNewsScraper(unittest.TestCase):
    def setUp(self):
        # Initialize the NewsScraper instance
        self.scraper = NewsScraper('https://www.aljazeera.com/')

    @patch('requests.get')
    @patch('bs4.BeautifulSoup')
    def test_scrape_headlines(self, mock_beautifulsoup, mock_requests):
        # Mocking response from requests.get
        mock_response = mock_requests.return_value
        mock_response.text = 'Mock HTML content'

        # Mocking BeautifulSoup instance
        mock_soup = mock_beautifulsoup.return_value
        mock_soup.find_all.return_value = [{'title': 'Mock headline 1'}, {'title': 'Mock headline 2'}]

        # Call the method to be tested
        headlines = self.scraper.scrape_headlines('Python', 'Technology', 1)

        # Assert the expected behavior
        self.assertEqual(len(headlines), 2)
        self.assertEqual(headlines[0]['title'], 'Mock headline 1')
        self.assertEqual(headlines[1]['title'], 'Mock headline 2')

    @patch('requests.get')
    @patch('bs4.BeautifulSoup')
    def test_scrape_news_details(self, mock_beautifulsoup, mock_requests):
        # Mocking response from requests.get
        mock_response = mock_requests.return_value
        mock_response.text = 'Mock HTML content'

        # Mocking BeautifulSoup instance
        mock_soup = mock_beautifulsoup.return_value
        mock_soup.find.return_value = {'text': 'Mock article content'}

        # Call the method to be tested
        title, date, description, picture = self.scraper.scrape_news_details('https://apnews.com/article/1')

        # Assert the expected behavior
        self.assertEqual(title, 'Mock article title')
        self.assertEqual(date, 'Mock article date')
        self.assertEqual(description, 'Mock article description')
        self.assertEqual(picture, 'Mock article picture')

    def test_contains_money(self):
        # Test contains_money method
        text_with_money = 'This is a text with $100'
        text_without_money = 'This is a text without money'

        self.assertTrue(self.scraper.contains_money(text_with_money))
        self.assertFalse(self.scraper.contains_money(text_without_money))

    def tearDown(self):
        # Clean up any resources used in the tests
        pass

if __name__ == '__main__':
    unittest.main()
