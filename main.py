import asyncio
from specialized.scraper import NewsScraperAgent
from specialized.summarizer import SummarizerAgent
from specialized.sentiment import SentimentAgent
from specialized.trend import TrendAgent
from specialized.broadcaster import BroadcastAgent
from core.models import IntelligenceReport

async def main():
    print("🚀 Initializing AI News Intelligence Agents...")
    
    # 1. Scraping Agent: Gathering the latest news
    scraper = NewsScraperAgent()
    news_items = await scraper.run()
    
    if not news_items:
        print("⚠️ No news fetched. Exiting...")
        return

    # 2. Summarization Agent: Condensing and focusing
    summarizer = SummarizerAgent()
    summarized_news = await summarizer.run(news_items[:5]) # Limiting for demo

    # 3. Sentiment Agent: Gauging the tone/impact
    sentiment_analyzer = SentimentAgent()
    sentimented_news = await sentiment_analyzer.run(summarized_news)

    # 4. Trend Agent: Identifying key technological tags
    trend_tracker = TrendAgent()
    trended_news = await trend_tracker.run(sentimented_news)

    # 5. Broadcast Agent: Distributing knowledge via Telegram
    broadcaster = BroadcastAgent()
    final_report = await broadcaster.run(trended_news)

    print("\n------------------------------")
    print("📡 FINAL BROADCAST REPORT:")
    print(f"Total News Processed: {len(final_report.articles)}")
    if final_report.top_story:
        print(f"🔥 TOP STORY: {final_report.top_story.title}")
        print(f"🔹 SUMMARY: {final_report.top_story.ai_summary}")
        print(f"✅ Sent to Telegram with Chat ID: {broadcaster.chat_id}")
    print("------------------------------\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by user.")
