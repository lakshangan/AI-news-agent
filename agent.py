import feedparser
import requests
import re
import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# ===================== LOAD ENV =====================
load_dotenv()  # Loads .env locally; ignored in GitHub Actions

# ===================== TELEGRAM =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("BOT_TOKEN or CHAT_ID missing. Check .env or GitHub Secrets.")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    })
    print("Telegram:", r.status_code, r.text)

# ===================== STORAGE =====================
def load_seen(file):
    if os.path.exists(file):
        return set(open(file).read().splitlines())
    return set()

def save_seen(file, value):
    with open(file, "a") as f:
        f.write(value + "\n")

seen_news = load_seen("seen_news.txt")
seen_jobs = load_seen("seen_jobs.txt")

# ===================== AI NEWS SOURCES =====================
AI_FEEDS = {
    "OpenAI": "https://openai.com/blog/rss.xml",
    "DeepMind": "https://deepmind.google/blog/rss.xml",
    "Hugging Face": "https://huggingface.co/blog/rss.xml",
    "Hacker News": "https://hnrss.org/newest?q=AI"
}

# ===================== JOB SOURCES =====================
JOB_FEEDS = [
    "https://www.indeed.com/rss?q=software+developer+india",
    "https://www.indeed.com/rss?q=blockchain+developer",
    "https://remoteok.com/remote-dev-jobs.rss",
    "https://weworkremotely.com/categories/remote-programming-jobs.rss"
]

DEV_KEYWORDS = [
    "developer", "software engineer", "backend", "frontend",
    "full stack", "web developer", "blockchain", "web3", "solidity"
]

SALARY_HINTS = [
    r"40,?000", r"₹", r"4\s?lpa", r"5\s?lpa", r"package", r"salary"
]

def is_dev_role(text):
    return any(k in text.lower() for k in DEV_KEYWORDS)

def has_salary_intent(text):
    return any(re.search(p, text.lower()) for p in SALARY_HINTS)

# ===================== TIME (IST SAFE) =====================
now_ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
label = "🌅 Morning Update" if now_ist.hour < 12 else "🌙 Night Update"

# ===================== MESSAGE =====================
msg = (
    f"🤖 <b>Your AI & Job Update</b>\n"
    f"🗓 {now_ist.strftime('%d %b %Y')}\n\n"
    f"<i>Here’s what we tracked for you.</i>\n\n"
)

# ===================== AI NEWS =====================
msg += "🧠 <b>AI — What’s Trending</b>\n"
news_added = 0

for name, feed_url in AI_FEEDS.items():
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:1]:
        if entry.link in seen_news:
            continue
        seen_news.add(entry.link)
        save_seen("seen_news.txt", entry.link)
        msg += f"• <b>{name}:</b> {entry.title}\n"
        news_added += 1
        break

if news_added == 0:
    msg += "• No new high-signal updates\n"

# ===================== JOBS =====================
msg += "\n💼 <b>Development Jobs (₹40k+)</b>\n"
jobs_added = 0

for feed_url in JOB_FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:3]:
        if entry.link in seen_jobs:
            continue

        text = (entry.title + " " + entry.get("summary", "")).lower()

        if is_dev_role(text) and has_salary_intent(text):
            seen_jobs.add(entry.link)
            save_seen("seen_jobs.txt", entry.link)

            note = (
                "Good blockchain opportunity."
                if "blockchain" in text or "web3" in text
                else "Solid development role."
            )

            msg += (
                f"\n🔹 <b>{entry.title}</b>\n"
                f"👉 Action: View & Apply\n"
                f"🔗 <a href='{entry.link}'>Open role</a>\n"
                f"<i>Note: {note}</i>\n"
            )
            jobs_added += 1
            break

if jobs_added == 0:
    msg += "• No strong development roles right now\n"

msg += "\n<i>Next update arrives at 10:00.</i>"

# ===================== SEND =====================
send_telegram(msg)