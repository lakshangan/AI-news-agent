import asyncio
from typing import List
from core.base import BaseAgent
from core.models import Article, AnalyzedArticle
import os
import google.generativeai as genai

class SummarizerAgent(BaseAgent):
    def __init__(self, use_mock: bool = False):
        super().__init__("Summarizer")
        self.use_mock = use_mock
        self.api_key = os.getenv("GEMINI_API_KEY")

        if self.api_key:
            self.log("Gemini API key found. Initializing AI engine...")
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.log("No Gemini API key found. Defaulting to Mock mode.")
            self.use_mock = True

    async def run(self, input_articles: List[Article]) -> List[AnalyzedArticle]:
        self.log(f"Processing {len(input_articles)} articles for summarization...")
        
        analyzed = []
        for article in input_articles:
            if self.use_mock:
                summary = f"MOCK SUMMARY: {article.title[:50]}... This is a simulated insight."
            else:
                summary = await self._call_llm(article.title, article.summary or "")
            
            item = AnalyzedArticle(**article.dict())
            item.ai_summary = summary
            analyzed.append(item)
            
        self.log("Completed summarization.")
        return analyzed

    async def _call_llm(self, title: str, body: str):
        try:
            # Customized prompt for more personal feel
            prompt = f"Explain this AI news to my friend Lakshan in 1-2 friendly, professional sentences. Focus on why it matters:\nTitle: {title}\nContent: {body}"
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            return response.text.strip()
        except Exception as e:
            self.error(f"Gemini Call Failed: {e}")
            return f"Thinking about this story: {title[:20]}..."
