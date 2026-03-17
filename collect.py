import feedparser
import json
import os
from datetime import date, datetime

# ─── ADD OR REMOVE BLOGS HERE ─────────────────────────────────────
BLOGS = [
    {"name": "HubSpot Marketing",  "rss": "https://blog.hubspot.com/marketing/rss.xml",       "topic": "Marketing"},
    {"name": "Neil Patel",         "rss": "https://neilpatel.com/blog/feed/",                 "topic": "Marketing"},
    {"name": "Smashing Magazine",  "rss": "https://www.smashingmagazine.com/feed/",            "topic": "Design"},
    {"name": "Creative Bloq",      "rss": "https://www.creativebloq.com/rss",                 "topic": "Design"},
    {"name": "TechCrunch",         "rss": "https://techcrunch.com/feed/",                     "topic": "Tech"},
    {"name": "The Verge",          "rss": "https://www.theverge.com/rss/index.xml",            "topic": "Tech"},
]

POSTS_PER_BLOG = 5
# ──────────────────────────────────────────────────────────────────

def collect_feed(blog: dict) -> list:
    print(f"  Fetching: {blog['name']}...")
    try:
        feed = feedparser.parse(blog["rss"])
        posts = []
        for entry in feed.entries[:POSTS_PER_BLOG]:
            posts.append({
                "source":    blog["name"],
                "topic":     blog["topic"],
                "title":     entry.get("title", "No title"),
                "url":       entry.get("link", ""),
                "summary":   entry.get("summary", "")[:300],
                "published": entry.get("published", "Unknown date"),
            })
        print(f"  ✅ Got {len(posts)} posts from {blog['name']}")
        return posts
    except Exception as e:
        print(f"  ❌ Failed {blog['name']}: {e}")
        return []

def run():
    print(f"\n🚀 Starting daily blog collection — {date.today()}\n")
    
    all_posts = []
    for blog in BLOGS:
        posts = collect_feed(blog)
        all_posts.extend(posts)

    by_topic = {}
    for post in all_posts:
        topic = post["topic"]
        if topic not in by_topic:
            by_topic[topic] = []
        by_topic[topic].append(post)

    output = {
        "date":        str(date.today()),
        "generated":   datetime.utcnow().isoformat() + "Z",
        "total_posts": len(all_posts),
        "by_topic":    by_topic,
        "all_posts":   all_posts,
    }

    os.makedirs("outputs", exist_ok=True)
    filename = f"outputs/posts_{date.today()}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    with open("outputs/latest.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Done! Collected {len(all_posts)} posts from {len(BLOGS)} blogs")
    print(f"📁 Saved to: {filename}")
    print(f"\n📊 Breakdown by topic:")
    for topic, posts in by_topic.items():
        print(f"  {topic}: {len(posts)} posts")

if __name__ == "__main__":
    run()
