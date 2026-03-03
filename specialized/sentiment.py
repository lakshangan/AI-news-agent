import random
from typing import List
from core.base import BaseAgent
from core.models import AnalyzedArticle

class SentimentAgent(BaseAgent):
    def __init__(self):
        super().__init__("SentimentAnalyzer")
        self.keywords = {
            "Positive": ["breakthrough", "growth", "new", "success", "innovative", "advanced"],
            "Negative": ["risk", "ban", "slowdown", "concern", "failure", "threat"]
        }

    async def run(self, input_data: List[AnalyzedArticle]) -> List[AnalyzedArticle]:
        self.log(f"Analyzing sentiment for {len(input_data)} news pieces...")
        
        for article in input_data:
            text = (article.title + (article.ai_summary or "")).lower()
            
            # Simple but functional keyword-based sentiment logic
            # Could be upgraded to an LLM call for better results
            pos_score = sum(1 for word in self.keywords["Positive"] if word in text)
            neg_score = sum(1 for word in self.keywords["Negative"] if word in text)
            
            if pos_score > neg_score:
                article.sentiment = "Positive"
                article.sentiment_score = 0.5 + (0.1 * pos_score)
            elif neg_score > pos_score:
                article.sentiment = "Negative"
                article.sentiment_score = -0.5 - (0.1 * neg_score)
            else:
                article.sentiment = "Neutral"
                article.sentiment_score = 0.0
                
            self.log(f"Sentiment for '{article.title[:20]}...': {article.sentiment}")

        self.log("Sentiment analysis completed.")
        return input_data
