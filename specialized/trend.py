from typing import List
from core.base import BaseAgent
from core.models import AnalyzedArticle
import re

class TrendAgent(BaseAgent):
    def __init__(self):
        super().__init__("TrendTracker")
        self.popular_trends = [
            "LLM", "Generative AI", "NLP", "Robotics", "Ethics", "Hardware",
            "GPU", "Open Source", "Market Share", "Startups", "Policy", "Scaling"
        ]

    async def run(self, input_articles: List[AnalyzedArticle]) -> List[AnalyzedArticle]:
        self.log(f"Categorizing {len(input_articles)} news articles by trend...")
        
        for article in input_articles:
            text = (article.title + (article.ai_summary or "")).upper()
            
            # Extract mentions of popular trends
            article.trends = [trend for trend in self.popular_trends if trend.upper() in text]
            if not article.trends:
                article.trends = ["Other"]
            
            # Simple importance logic based on title length and trend count
            article.importance_score = min(len(article.title) / 100.0 + (0.1 * len(article.trends)), 1.0)
            self.log(f"Identified trends: {', '.join(article.trends)}")

        self.log("News trend categorization completed.")
        return input_articles
