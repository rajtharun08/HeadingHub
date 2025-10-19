import requests
from bs4 import BeautifulSoup
import logging
from textblob import TextBlob

# basic logging config. we'll just see info-level messages and up.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# set a common user-agent to avoid getting blocked by anti-scraping measures.
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

def scrape_and_analyze_headlines():
    """
    scrapes bbc news and analyzes sentiment.
    returns a list of formatted headlines. returns an empty list if anything fails.
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
        # the website's html will change. this selector will need to be updated eventually.
        headlines_html = soup.find_all('h2', {'data-testid': 'card-headline'}, limit=10)

        if not headlines_html:
            logging.warning("selector found no headlines. website structure has likely changed.")
            return []
        
        logging.info(f"found {len(headlines_html)} headlines. analyzing sentiment...")
        for h in headlines_html:
            headline_text = h.get_text(strip=True)
            
            # run sentiment analysis on the clean text.
            blob = TextBlob(headline_text)
            polarity = blob.sentiment.polarity
            emoji = get_sentiment_emoji(polarity)
            
            formatted_headlines.append(f"{headline_text} {emoji}")

    # catch network-related issues.
    except requests.exceptions.RequestException as e:
        logging.error(f"network error during scraping: {e}")
        return []
    # catch any other unexpected problems.
    except Exception as e:
        logging.error(f"an unexpected error occurred: {e}")
        return []

    return formatted_headlines

# standard boilerplate to make the script testable.
# this block only runs if you execute `python news_scraper.py` directly.
if __name__ == '__main__':
    news = scrape_and_analyze_headlines()
    if news:
        print("\n--- today's top headlines (with sentiment) ---")
        for i, item in enumerate(news):
            print(f"{i+1}. {item}")
    else:
        print("\ncould not retrieve news. check the log for details.")