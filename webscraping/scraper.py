from bs4 import BeautifulSoup
import requests
from data_extractor import extract_article_data
from csv_writer import save_to_csv

# Define URLs for NPR, Nature, and other reputable environmental journalism sources
urls = [
    "https://www.npr.org/sections/environment",
    "https://www.nature.com/subjects/water-resources",
    # Add more environmental journalism sources here
]

def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to retrieve: {url}")
        return None

def scrape_articles(url_list):
    articles = []
    for url in url_list:
        soup = get_soup(url)
        if soup:
            articles.extend(extract_article_data(soup, url))
    return articles

if __name__ == "__main__":
    articles_data = scrape_articles(urls)  # Loop over the list of URLs
    save_to_csv(articles_data, "water_effects.csv")
