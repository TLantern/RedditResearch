# reddit_scraper.py
import os
import praw
from dotenv import load_dotenv

load_dotenv()

class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
        )

    def fetch_posts(self, subreddit: str, limit: int = 100, timeframe: str = "week"):
        """
        Returns a list of dicts: [{'id': ..., 'title': ..., 'text': ..., 'score': ...}, ...]
        timeframe: one of 'day','week','month','year','all'
        """
        sub = self.reddit.subreddit(subreddit)
        posts = []
        for post in getattr(sub, 'top')(time_filter=timeframe, limit=limit):
            text = post.selftext or ""
            posts.append({
                "id": post.id,
                "title": post.title,
                "text": text,
                "score": post.score
            })
        return posts
