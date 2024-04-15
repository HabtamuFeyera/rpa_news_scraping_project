import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re 
import pandas as pd
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

class NewsScraper:
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    def scrape_headlines(self, search_phrase, news_category, num_months):
        try:
            self.logger.info(f"Scraping headlines from {self.url}...")
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            headlines = []
            for headline in soup.find_all('h2'):
                headline_text = headline.text.strip()
                if search_phrase.lower() in headline_text.lower() and news_category.lower() in response.url.lower():
                    headlines.append({
                        'title': headline_text,
                        'link': headline.find('a')['href']
                    })
            self.logger.info(f"Found {len(headlines)} headlines matching the search criteria.")
            return headlines
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch headlines: {e}")
            return []

    def scrape_news_details(self, article_url):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.visibility_of_element_located((By.TAG_NAME, 'h1'))
            )

            response = requests.get(article_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h1').text.strip()
            date = soup.find('time')['datetime']
            description = soup.find('div', class_='article-body').text.strip()
            picture = soup.find('img')['src']
            return title, date, description, picture
        except TimeoutException:
            self.logger.warning("Timeout occurred while waiting for article details to load.")
            return None, None, None, None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch news details: {e}")
            return None, None, None, None
        except Exception as e:
            self.logger.error(f"An error occurred while scraping article details: {e}")
            return None, None, None, None

    @staticmethod
    def contains_money(text):
        money_pattern = r'\$[0-9,.]+|\d+ dollars|\d+ USD'
        return bool(re.search(money_pattern, text))

    @staticmethod   
    def save_to_excel(data, file_path):
        if not data:
            print("No data to save. Exiting.")
            return
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)

    @staticmethod
    def download_picture(url, file_path):
        urllib.request.urlretrieve(url, file_path)
