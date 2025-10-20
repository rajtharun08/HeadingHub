import requests
from bs4 import BeautifulSoup
import logging
from textblob import TextBlob
from deep_translator import GoogleTranslator

# basic logging config.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# set a common user-agent to avoid getting blocked.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_sentiment_emoji(polarity):
    """assigns an emoji based on a sentiment score."""
    # using a 0.1 threshold to avoid flagging slightly-off-neutral headlines.
    if polarity > 0.1:
        return "😊"
    elif polarity < -0.1:
        return "😞"
    else:
        return "😐"

def scrape_and_analyze_headlines(language_code='en'):
    """
    scrapes bbc news, analyzes sentiment, and optionally translates.
    returns an empty list if anything fails.
    """
    url = "https://www.bbc.com/news"
    formatted_headlines = []
    
    try:
        logging.info(f"fetching news from {url}...")
        response = requests.get(url, headers=HEADERS, timeout=10)
        # this is important - it'll error out if we get a 404 or 503 response.
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # note: this is the most fragile part of the scraper.
        # the website's html will change, and this selector will need to be updated.
        headlines_html = soup.find_all('h2', {'data-testid': 'card-headline'}, limit=10)

        if not headlines_html:
            logging.warning("selector found no headlines. website structure has likely changed.")
            return []
        
        logging.info(f"found {len(headlines_html)} headlines. analyzing and translating...")
        for h in headlines_html:
            headline_text = h.get_text(strip=True)
            
            blob = TextBlob(headline_text)
            polarity = blob.sentiment.polarity
            emoji = get_sentiment_emoji(polarity)
            
            final_headline_string = f"{headline_text} {emoji}"

            if language_code != 'en':
                try:
                    # using deep-translator here because it's more reliable than textblob's.
                    translation = GoogleTranslator(source='auto', target=language_code).translate(headline_text)
                    final_headline_string += f"\n   ➤ {translation}"
                except Exception as e:
                    logging.error(f"could not translate '{headline_text}'. error: {e}")
                    final_headline_string += "\n   ➤ (translation failed)"
            
            formatted_headlines.append(final_headline_string)

    # catch network-related issues specifically.
    except requests.exceptions.RequestException as e:
        logging.error(f"network error during scraping: {e}")
        return []
    # catch any other unexpected problems.
    except Exception as e:
        logging.error(f"an unexpected error occurred: {e}")
        return []

    return formatted_headlines

# this block only runs if you execute `python news_scraper.py` directly.
if __name__ == '__main__':
    news = scrape_and_analyze_headlines(language_code='hi')
    if news:
        for item in news:
            print(f"{item}\n")