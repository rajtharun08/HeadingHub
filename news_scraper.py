import requests
from bs4 import BeautifulSoup
import logging
from textblob import TextBlob
# we're adding the new, more reliable translator library.
from googletrans import Translator

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

# we're adding a 'language_code' parameter, which defaults to english ('en').
def scrape_and_analyze_headlines(language_code='en'):
    """
    scrapes bbc news, analyzes sentiment, and optionally translates.
    returns a list of formatted headlines. returns an empty list if anything fails.
    """
    url = "https://www.bbc.com/news"
    formatted_headlines = []
    # create an instance of the translator.
    translator = Translator()

    try:
        logging.info(f"fetching news from {url}...")
        response = requests.get(url, headers=HEADERS, timeout=10)
        # this is important - it'll error out if we get a 404 or 503 response.
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # note: this selector is the most fragile part of the scraper and may need future updates.
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
            
            # start with the original english headline and its emoji.
            final_headline_string = f"{headline_text} {emoji}"

            # now, if the user requested a language other than english, we translate.
            if language_code != 'en':
                try:
                    # use the new googletrans library for a reliable translation.
                    translation = translator.translate(headline_text, dest=language_code)
                    final_headline_string += f"\n   ➤ {translation.text}"
                except Exception as e:
                    # if it fails, just add a note and move on without crashing.
                    logging.error(f"could not translate '{headline_text}'. error: {e}")
                    final_headline_string += "\n   ➤ (translation failed)"
            
            formatted_headlines.append(final_headline_string)

    except requests.exceptions.RequestException as e:
        logging.error(f"network error during scraping: {e}")
        return []
    except Exception as e:
        logging.error(f"an unexpected error occurred: {e}")
        return []

    return formatted_headlines

# we'll update the test block to check both english and a translated language.
if __name__ == '__main__':
    # first, test the default english version
    news_en = scrape_and_analyze_headlines()
    if news_en:
        print("\n--- today's top headlines (english) ---")
        for i, item in enumerate(news_en):
            print(f"{i+1}. {item}\n")
    else:
        print("\ncould not retrieve english news. check the log for details.")

    # a separator to make the output clear
    print("\n" + "="*50 + "\n")

    # now, let's test the translation with tamil ('ta').
    news_translated = scrape_and_analyze_headlines(language_code='ta')
    if news_translated:
        print("\n--- today's top headlines (translated to hindi) ---")
        for i, item in enumerate(news_translated):
            print(f"{i+1}. {item}\n")
    else:
        print("\ncould not retrieve translated news. check the log for details.")