import feedparser
import asyncio
from typing import List
from core.base import BaseAgent
from core.models import Article

class NewsScraperAgent(BaseAgent):
    def __init__(self, feeds: List[str] = None):
        super().__init__("NewsScraper")
        self.feeds = feeds or [
            "https://news.google.com/rss/search?q=Artificial+Intelligence&hl=en-US&gl=US&ceid=US:en",
            "https://techcrunch.com/category/artificial-intelligence/feed/",
            "https://openai.com/news/rss.xml"
        ]

    async def run(self, input_data: None = None) -> List[Article]:
        self.log(f"Starting news search across {len(self.feeds)} feeds...")
        articles = []
        
        # In a real scenario, use asyncio to fetch parallel
        for feed_url in self.feeds:
            try:
                self.log(f"Fetching from: {feed_url}")
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]: # Take top 5 from each
                    article = Article(
                        title=entry.get('title', 'N/A'),
                        link=entry.get('link', ''),
                        summary=entry.get('summary', entry.get('description', '')),
                        published=entry.get('published', 'N/A'),
                        source=feed_url.split('/')[2] # Simple extraction
                    )
                    articles.append(article)
            except Exception as e:
                self.error(f"Failed to parse {feed_url}: {e}")

        self.log(f"Successfully scraped {len(articles)} articles.")
        return articles
