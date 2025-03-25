import feedparser
import requests
from bs4 import BeautifulSoup

def scrape_the_hindu(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    news_articles = []
    for article in soup.find_all("div", class_="story-card"):  # Adjust the class based on the website
        title = article.find("h2").text.strip()
        description = article.find("p").text.strip()
        news_articles.append(f"{title}: {description}")

    return " ".join(news_articles)

def fetch_news(category="general", region="india"):
    # Define RSS feed URLs and scraping URLs for different categories and regions
    rss_feeds = {
        "general": {
            "india": [
                "http://feeds.bbci.co.uk/news/world/asia/india/rss.xml",  # BBC India
                "https://www.thehindu.com/news/national/feeder/default.rss",  # The Hindu National
                "https://indianexpress.com/section/india/feed/",  # Indian Express
            ],
            "international": [
                "http://feeds.bbci.co.uk/news/world/rss.xml",  # BBC World
                "https://www.thehindu.com/news/international/feeder/default.rss",  # The Hindu International
            ],
        },
        "politics": {
            "india": [
                "http://feeds.bbci.co.uk/news/politics/rss.xml",  # BBC Politics
                "https://www.thehindu.com/news/national/feeder/default.rss",  # The Hindu National
            ],
            "international": [
                "http://feeds.bbci.co.uk/news/politics/rss.xml",  # BBC Politics
                "https://www.thehindu.com/news/international/feeder/default.rss",  # The Hindu International
            ],
        },
        "technology": {
            "india": [
                "http://feeds.bbci.co.uk/news/technology/rss.xml",  # BBC Technology
                "https://www.thehindu.com/sci-tech/technology/feeder/default.rss",  # The Hindu Technology
            ],
            "international": [
                "http://feeds.bbci.co.uk/news/technology/rss.xml",  # BBC Technology
                "https://www.thehindu.com/sci-tech/technology/feeder/default.rss",  # The Hindu Technology
            ],
        },
        "sports": {
            "india": [
                "http://feeds.bbci.co.uk/news/sport/rss.xml",  # BBC Sports
                "https://www.thehindu.com/sport/feeder/default.rss",  # The Hindu Sports
            ],
            "international": [
                "http://feeds.bbci.co.uk/news/sport/rss.xml",  # BBC Sports
                "https://www.thehindu.com/sport/feeder/default.rss",  # The Hindu Sports
            ],
        },
    }

    # Add scraping URLs for websites without RSS feeds
    scraping_urls = {
        "general": {
            "india": [
                "https://www.thehindu.com/news/national/",  # The Hindu National
            ],
        },
    }

    # Fetch news from RSS feeds
    news_text = ""
    for rss_url in rss_feeds.get(category, {}).get(region, []):
        print("Fetching from RSS feed:", rss_url)  # Debug: Print the RSS feed URL
        try:
            feed = feedparser.parse(rss_url)
            if not feed.entries:
                print("No entries found in the RSS feed:", rss_url)  # Debug: Print if no entries are found
                continue

            for entry in feed.entries:
                title = entry.get("title", "") or ""
                description = entry.get("description", "") or ""
                news_text += f"{title}: {description}\n\n"  # Add newlines for better readability
        except Exception as e:
            print(f"Error parsing RSS feed {rss_url}: {e}")

    # Fetch news from scraping URLs
    for scrape_url in scraping_urls.get(category, {}).get(region, []):
        print("Scraping from:", scrape_url)  # Debug: Print the scraping URL
        try:
            news_text += scrape_the_hindu(scrape_url) + "\n\n"  # Add newlines for better readability
        except Exception as e:
            print(f"Error scraping {scrape_url}: {e}")

    # Debug: Print the fetched news text
    print("Fetched news text length:", len(news_text))  # Debug: Print the length of the fetched text
    print("Fetched news text:", news_text)  # Debug: Print the full news text

    return news_text