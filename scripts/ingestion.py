import feedparser
import os
import json
from bs4 import BeautifulSoup

def scrape_rss_trends(feed_url="https://techcrunch.com/category/artificial-intelligence/feed/", limit=5):
    """
    Scrape trending topics from a public RSS feed.
    No API keys required!
    """
    print(f"Fetching RSS feed from {feed_url}...")
    feed = feedparser.parse(feed_url)
    
    trending_topics = []
    
    for entry in feed.entries[:limit]:
        # Clean HTML tags from the summary if present
        soup = BeautifulSoup(entry.summary, "html.parser")
        clean_summary = soup.get_text()[:500] # First 500 chars for context
        
        trending_topics.append({
            "title": entry.title,
            "url": entry.link,
            "selftext": clean_summary
        })
            
    return trending_topics

if __name__ == "__main__":
    print("Starting AACE Data Ingestion (RSS Mode)...")
    
    # We use a public RSS feed here (e.g., TechCrunch AI news)
    # This completely bypasses the need for Reddit API keys!
    feed_url = "https://techcrunch.com/category/artificial-intelligence/feed/"
    trends = scrape_rss_trends(feed_url, limit=3)
    
    # Save the scraped data to a JSON file for the Engine layer to pick up
    os.makedirs("data", exist_ok=True)
    with open("data/trending_topics.json", "w") as f:
        json.dump(trends, f, indent=4)
        
    print(f"Successfully scraped {len(trends)} trending topics.")
