import requests
from bs4 import BeautifulSoup
import logging

# Configure basic logging to show timestamps, log level, and the message.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set a User-Agent header to mimic a real browser.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_headlines():
    """
    Scrapes top headlines from BBC News and returns them as a list.
    Returns an empty list on failure.
    """
    url = "https://www.bbc.com/news"
    scraped_headlines = []

    try:
        logging.info(f"Fetching news from {url}...")
        response = requests.get(url, headers=HEADERS, timeout=10)
        # This will raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        
        headlines = soup.find_all('h2', {'data-testid': 'card-headline'}, limit=10)

        if not headlines:
            logging.warning("No headlines found. The website structure may have changed.")
            return []
        
        # Loop through the found headlines and add their text to our list
        for h in headlines:
            scraped_headlines.append(h.get_text(strip=True))

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to scrape the website due to a network error: {e}")
        return [] # Return an empty list to signify failure
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return [] # Return an empty list

    return scraped_headlines

# The test block now calls the function and then prints the results.
if __name__ == '__main__':
    news = scrape_headlines()
    if news:
        print("\n--- Today's Top Headlines ---")
        for i, item in enumerate(news):
            print(f"{i+1}. {item}")
    else:
        print("\nCould not retrieve news. Check the log for details.")