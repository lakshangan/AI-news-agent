import aiohttp
from typing import List
from core.base import BaseAgent
from core.models import AnalyzedArticle, IntelligenceReport
import os
import asyncio

class BroadcastAgent(BaseAgent):
    def __init__(self, bot_token: str = None, chat_id: str = None):
        super().__init__("Broadcaster")
        self.bot_token = bot_token or os.getenv("BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("CHAT_ID")
        self.enabled = bool(self.bot_token and self.chat_id)
        
        if not self.enabled:
            self.error("No Telegram BOT_TOKEN or CHAT_ID found. Broadcasting will be disabled.")

    async def run(self, input_articles: List[AnalyzedArticle]) -> IntelligenceReport:
        # Create a final intelligence report
        top_story = max(input_articles, key=lambda x: x.importance_score) if input_articles else None
        
        report = IntelligenceReport(
            articles=input_articles,
            top_story=top_story
        )
        
        self.log(f"Summary Report Created with {len(input_articles)} entries.")
        self.log(f"Top Story identified: {top_story.title if top_story else 'N/A'}")

        if self.enabled:
            await self._send_to_telegram(report)
        else:
            self.log("Broadcast disabled. Report generated but not sent.")

        return report

    async def _send_to_telegram(self, report: IntelligenceReport):
        if not report.articles:
            return

        # Personalize Greeting
        header = f"🚀 *Hey Lakshan! Here is your AI Briefing* \n_{report.timestamp.strftime('%H:%M %d %b')}_\n\n"
        
        # Add Top Pick
        if report.top_story:
            top_section = f"⭐ *Top Selection for you:* \n[{report.top_story.title}]({report.top_story.link})\n" \
                          f"🔹 _{report.top_story.ai_summary or 'See article.'}_\n\n"
        else:
            top_section = ""

        # Brief list of others
        other_section = "📊 *Other stories I've collected:*\n"
        for art in report.articles[:3]:
            other_section += f"- [{art.title}]({art.link})\n"

        full_message = header + top_section + other_section

        # Send via Telegram API
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": full_message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        self.log("Broadcast successfully sent to Telegram!")
                    else:
                        rtext = await resp.text()
                        self.error(f"Telegram API Error (Status {resp.status}): {rtext}")
        except Exception as e:
            self.error(f"Failed to broadcast via Telegram: {e}")
