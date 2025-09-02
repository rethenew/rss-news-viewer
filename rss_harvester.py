# rss_harvester.py
import feedparser
from datetime import datetime
import hashlib
import json

FEEDS = [
    "https://news.samsung.com/global/feed",
    "https://news.google.com/rss/search?q=삼성전자+when:1d&hl=ko&gl=KR&ceid=KR:ko",
    "https://www.yna.co.kr/rss/all.xml",
    "https://www.hani.co.kr/rss/",
    "http://www.chosun.com/site/data/rss/rss.xml",
    "https://rss.mt.co.kr/rss/news.xml",
    "https://rss.etnews.com/ETnews.xml"
]

def make_id(entry):
    base = (entry.get("title") or "") + (entry.get("link") or "") + (entry.get("published", "") or "")
    return hashlib.sha256(base.encode("utf-8")).hexdigest()

def harvest():
    collected = []
    for feed_url in FEEDS:
        print(f"📡 피드 수집 중: {feed_url}")
        parsed = feedparser.parse(feed_url)
        for entry in parsed.entries:
            print("📰 수집한 기사:", entry.get("title", "제목 없음"))
            item = {
                "id": make_id(entry),
                "feed": feed_url,
                "title": entry.get("title"),
                "link": entry.get("link"),
                "summary": entry.get("summary", ""),
                "published": entry.get("published", ""),
                "collected_at": datetime.utcnow().isoformat()
            }
            collected.append(item)
    return collected

if __name__ == "__main__":
    print("🔍 RSS 수집 시작")
    results = harvest()
    print(f"✅ 총 {len(results)}개 수집됨.")
    with open("rss_output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("💾 JSON 파일 저장 완료!")
