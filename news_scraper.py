import requests
from bs4 import BeautifulSoup

# Set a User-Agent header to mimic a real browser.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_headlines():
    """Scrapes top headlines from BBC News and prints them."""
    url = "https://www.bbc.com/news"
    
    print("Fetching news from BBC...")
    response = requests.get(url, headers=HEADERS, timeout=10)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    

    # looks for any h2 tag with a specific data-testid attribute.
    headlines = soup.find_all('h2', {'data-testid': 'card-headline'}, limit=10)

    print("\n--- Today's Top Headlines ---")
    if headlines:
        for index, h in enumerate(headlines):
            print(f"{index + 1}. {h.get_text(strip=True)}")
    else:
        print("Could not find any headlines. The website structure may have changed.")


if __name__ == '__main__':
    scrape_headlines()
