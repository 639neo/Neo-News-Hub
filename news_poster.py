#!/usr/bin/env python3
"""
Neo News Hub — Autonomous News Poster v2
- Fetches latest AI/tech news via Tavily
- Tracks posted titles to avoid duplicates
- Posts unique articles to the blog API every run
"""
import os
import sys
import json
import hashlib
import subprocess
import requests
from datetime import datetime, timezone

BLOG_API = "http://localhost:8080/api/post"
WORKSPACE = "/home/ashin/.openclaw/workspace"
TAVILY_SCRIPT = f"{WORKSPACE}/skills/tavily-search-pro/lib/tavily_search.py"
VENV_PYTHON = "/home/ashin/.openclaw/venv/bin/python3"
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
POSTED_LOG = os.path.join(os.path.dirname(__file__), "posted_titles.json")

# loremflickr topics mapped to tag keywords
FLICKR_TOPICS = {
    "ai": "artificial+intelligence",
    "machine learning": "artificial+intelligence",
    "openai": "artificial+intelligence",
    "chatgpt": "artificial+intelligence",
    "gemini": "artificial+intelligence",
    "llm": "artificial+intelligence",
    "google": "technology",
    "nvidia": "technology",
    "robot": "robot",
    "chip": "microchip",
    "semiconductor": "microchip",
    "cybersecurity": "cybersecurity",
    "hacking": "cybersecurity",
    "quantum": "quantum",
    "space": "space",
    "meta": "technology",
    "microsoft": "technology",
    "apple": "technology",
    "default": "technology"
}

def load_posted():
    if os.path.exists(POSTED_LOG):
        with open(POSTED_LOG, "r") as f:
            return set(json.load(f))
    return set()

def save_posted(posted_set):
    # Keep last 500 entries
    lst = list(posted_set)[-500:]
    with open(POSTED_LOG, "w") as f:
        json.dump(lst, f)

def title_hash(title):
    return hashlib.md5(title.lower().strip()[:80].encode()).hexdigest()[:12]

def get_thumbnail(tags):
    topic = FLICKR_TOPICS["default"]
    for tag in tags:
        tl = tag.lower()
        for k, v in FLICKR_TOPICS.items():
            if k in tl:
                topic = v
                break
    lock = int(datetime.now().timestamp()) % 9999
    return f"https://loremflickr.com/1200/630/{topic}?lock={lock}"

def run_tavily(query, mode="news"):
    env = os.environ.copy()
    env["TAVILY_API_KEY"] = TAVILY_API_KEY
    result = subprocess.run(
        [VENV_PYTHON, TAVILY_SCRIPT, mode, query, "-n", "5", "--json", "--time", "day"],
        capture_output=True, text=True, env=env, timeout=30
    )
    if result.returncode != 0:
        print(f"Tavily error: {result.stderr[:200]}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        for line in reversed(result.stdout.strip().split('\n')):
            try:
                return json.loads(line)
            except:
                pass
        return None

def fetch_candidates():
    queries = [
        "latest artificial intelligence news today",
        "OpenAI Google DeepMind Meta AI announcement today",
        "tech industry news today 2025",
        "machine learning breakthrough research today",
        "cybersecurity AI development news",
        "NVIDIA AMD chip technology news",
    ]
    all_results = []
    for q in queries:
        data = run_tavily(q, "news")
        if data:
            results = data.get("results", data) if isinstance(data, dict) else data
            if isinstance(results, list):
                all_results.extend(results)
    return all_results

def pick_new_article(candidates, posted):
    """Return first candidate whose title hash isn't in posted set."""
    seen_this_run = set()
    for art in candidates:
        raw_title = art.get("title", "").strip()
        if not raw_title or not art.get("content"):
            continue
        h = title_hash(raw_title)
        if h in posted or h in seen_this_run:
            continue
        seen_this_run.add(h)
        return art, h
    return None, None

def build_post(art, extras):
    """Build a rich post from main article + related extras."""
    raw_title = art.get("title", "Tech News").strip()
    # Strip source suffix
    for sep in [" - ", " | ", " — ", " · "]:
        if sep in raw_title:
            raw_title = raw_title.split(sep)[0].strip()

    content_lines = [f"## {raw_title}\n"]

    main_body = art.get("content", art.get("snippet", "")).strip()
    if main_body:
        content_lines.append(main_body + "\n")
    url = art.get("url", "")
    if url:
        content_lines.append(f"[Read full story]({url})\n")

    # Add related articles
    added = 0
    for extra in extras:
        if added >= 3:
            break
        et = extra.get("title", "").strip()
        ec = extra.get("content", extra.get("snippet", "")).strip()
        eu = extra.get("url", "")
        if not et or not ec or et == art.get("title"):
            continue
        for sep in [" - ", " | ", " — ", " · "]:
            if sep in et:
                et = et.split(sep)[0].strip()
        content_lines.append(f"\n---\n\n### Also: {et}\n")
        content_lines.append(ec[:400] + ("…" if len(ec) > 400 else "") + "\n")
        if eu:
            content_lines.append(f"[Source]({eu})\n")
        added += 1

    date_str = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")
    content_lines.append(f"\n---\n*Published by Neo · {date_str}*")
    content = "\n".join(content_lines)

    # Excerpt
    excerpt = main_body[:240].strip()
    if len(main_body) > 240:
        excerpt += "…"

    # Tags
    tags = ["AI", "Tech"]
    cl = content.lower()
    tag_map = {
        "OpenAI": ["openai", "chatgpt", "gpt"],
        "Google": ["google", "gemini", "deepmind"],
        "Security": ["security", "cyber", "hack", "breach"],
        "Robotics": ["robot", "autonomous"],
        "Quantum": ["quantum"],
        "NVIDIA": ["nvidia", "gpu"],
        "Microsoft": ["microsoft", "azure", "copilot"],
        "Meta": ["meta", "llama"],
    }
    for label, keywords in tag_map.items():
        if any(kw in cl for kw in keywords):
            tags.append(label)
    tags = list(dict.fromkeys(tags))[:4]

    return {
        "title": raw_title,
        "content": content,
        "excerpt": excerpt,
        "author": "Neo",
        "tags": tags,
        "thumbnail": get_thumbnail(tags),
        "thumbnail_alt": raw_title,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }

def post_to_blog(post_data):
    try:
        resp = requests.post(BLOG_API, json=post_data, timeout=10)
        if resp.status_code == 201:
            result = resp.json()
            print(f"✅ Posted: {post_data['title'][:70]} (slug: {result.get('slug', '?')})")
            return True
        print(f"❌ API {resp.status_code}: {resp.text[:100]}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        return False

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching AI/tech news…")
    posted = load_posted()

    candidates = fetch_candidates()
    if not candidates:
        print("No candidates found.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(candidates)} candidates. Checking for new ones…")
    main_art, h = pick_new_article(candidates, posted)

    if not main_art:
        print("No new articles — all already posted. Skipping.")
        sys.exit(0)

    # Collect extras (different from main)
    extras = [c for c in candidates if c.get("title") != main_art.get("title") and c.get("content")]

    post_data = build_post(main_art, extras)
    success = post_to_blog(post_data)

    if success:
        posted.add(h)
        save_posted(posted)
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
