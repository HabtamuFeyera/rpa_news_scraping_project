import os
import logging
from datetime import datetime
from selenium import webdriver
from news_scraper import NewsScraper

def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

def validate_environment_variables(search_phrase, news_category, num_months_str):
    if not search_phrase:
        logger.error("SEARCH_PHRASE environment variable is not set. Exiting.")
        return False
    try:
        int(num_months_str)
    except ValueError:
        logger.warning("Invalid value for NUM_MONTHS. Defaulting to 1 month.")
    return True

def initialize_web_driver():
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--headless')  # Optional: Run in headless mode
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        raise


def close_web_driver(driver):
    try:
        driver.quit()
    except Exception as e:
        logger.warning(f"Failed to close WebDriver: {e}")

def main():
    search_phrase = "Can’t get enough of the total solar eclipse or got clouded out? Here are the next ones to watch for"  # Updated search phrase
    news_category = "science"  # No specific category
    num_months_str = "1"  # Scrape headlines from the last month
    excel_file_path = "output.xlsx"  # Default Excel file path

    if not validate_environment_variables(search_phrase, news_category, num_months_str):
        return

    logger.info("Starting news scraping process...")

    try:
        num_months = int(num_months_str)

        url = 'https://apnews.com/article/total-solar-eclipse-next-totality-c3bc0a68e1ad187729297296a5f582f9'
        logger.info(f"Scraping headlines from {url}...")

        driver = initialize_web_driver()
        scraper = NewsScraper(url, driver)

        # Rest of the code remains unchanged

        headlines = scraper.scrape_headlines(search_phrase, news_category, num_months)
        if not headlines:
            logger.info("No headlines found matching the search criteria.")
            return

        logger.info(f"Found {len(headlines)} headlines matching the search criteria.")

        data = []
        for headline in headlines:
            title, date, description, picture = scraper.scrape_news_details(url + headline['link'])
            if title is None or date is None:
                logger.warning(f"Failed to scrape details for headline: {headline['title']}")
                continue
            contains_search_phrase = search_phrase.lower() in (title.lower() + (description.lower() if description else ''))
            contains_money_flag = scraper.contains_money(title) or (description and scraper.contains_money(description))
            picture_filename = 'picture_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
            if picture:
                scraper.download_picture(picture, picture_filename)
            data.append({
                'title': title,
                'date': date,
                'description': description,
                'picture_filename': picture_filename,
                'contains_search_phrase': contains_search_phrase,
                'contains_money': contains_money_flag
            })
        
        scraper.save_to_excel(data, excel_file_path)
        logger.info(f"Scraping completed. Data saved to {excel_file_path}")

    except Exception as e:
        logger.error(f"An error occurred during scraping: {e}")

    finally:
        close_web_driver(driver)
        logger.info("Exiting news scraping process.")

if __name__ == "__main__":
    logger = setup_logging()
    main()
