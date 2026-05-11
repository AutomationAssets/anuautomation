import praw
import os
import json
from dotenv import load_dotenv

# Load environment variables (for local testing)
load_dotenv()

def scrape_reddit_trends(subreddit_name="SaaS", limit=10):
    """
    Scrape trending posts from a specific subreddit to identify content gaps.
    Requires REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET.
    """
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("Warning: Reddit API keys not found. Using fallback mock data.")
        return get_mock_trends()

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="AACE Bot v1.0"
    )

    trending_topics = []
    subreddit = reddit.subreddit(subreddit_name)
    
    # Get hot posts
    for post in subreddit.hot(limit=limit):
        if not post.stickied:
            trending_topics.append({
                "title": post.title,
                "score": post.score,
                "num_comments": post.num_comments,
                "url": post.url,
                "selftext": post.selftext[:500] # First 500 chars for context
            })
            
    return trending_topics

def get_mock_trends():
    """Fallback data for local testing without API keys"""
    return [
        {
            "title": "What's the best AI writing tool for long-form blog posts in 2024?",
            "score": 150,
            "num_comments": 45,
            "selftext": "I'm looking for an AI tool that doesn't just sound like ChatGPT. Ideally something with SEO built-in. Jasper? Surfer? Thoughts?"
        }
    ]

if __name__ == "__main__":
    print("Starting AACE Data Ingestion...")
    trends = scrape_reddit_trends("SaaS", limit=5)
    
    # Save the scraped data to a JSON file for the Engine layer to pick up
    os.makedirs("data", exist_ok=True)
    with open("data/trending_topics.json", "w") as f:
        json.dump(trends, f, indent=4)
        
    print(f"Successfully scraped {len(trends)} trending topics.")
