from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Article(BaseModel):
    title: str
    link: str
    summary: Optional[str] = None
    published: str
    source: str

class AnalyzedArticle(Article):
    ai_summary: Optional[str] = None
    sentiment: Optional[str] = None # Positive, Neutral, Negative
    sentiment_score: Optional[float] = 0.0
    trends: List[str] = []
    importance_score: float = 0.0

class IntelligenceReport(BaseModel):
    timestamp: datetime = datetime.now()
    articles: List[AnalyzedArticle]
    top_story: Optional[AnalyzedArticle] = None
