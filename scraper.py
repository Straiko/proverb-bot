import asyncio
import aiohttp
import json
import re
from bs4 import BeautifulSoup

CATEGORIES = {
    "vremena-goda": {"id": 1, "name": "времена года", "emoji": "🍂"},
    "korotkie": {"id": 2, "name": "короткие", "emoji": "📝"},
    "narodnye": {"id": 3, "name": "народные", "emoji": "🏠"},
    "ob-uchenii": {"id": 4, "name": "об учении", "emoji": "📚"},
    "o-glugosti": {"id": 5, "name": "о глупости", "emoji": "🤦"},
    "o-dobre": {"id": 6, "name": "о добре", "emoji": "😇"},
    "o-druzhbe": {"id": 7, "name": "о дружбе", "emoji": "🤝"},
    "o-zdorove": {"id": 8, "name": "о здоровье", "emoji": "💪"},
    "o-znaniyah": {"id": 9, "name": "о знаниях", "emoji": "🧠"},
    "o-knige": {"id": 10, "name": "о книге", "emoji": "📖"},
    "o-leni": {"id": 11, "name": "о лени", "emoji": "😴"},
    "o-lyubvi": {"id": 12, "name": "о любви", "emoji": "❤️"},
    "o-mire": {"id": 13, "name": "о мире", "emoji": "☮️"},
    "o-prirode": {"id": 14, "name": "о природе", "emoji": "🌿"},
    "o-rodine": {"id": 15, "name": "о родине", "emoji": "🇷🇺"},
    "o-russkom-yazyke": {"id": 16, "name": "о русском языке", "emoji": "🗣️"},
    "o-seme": {"id": 17, "name": "о семье", "emoji": "👨‍👩‍👧‍👦"},
    "o-sile-razuma": {"id": 18, "name": "о силе разума", "emoji": "💡"},
    "o-trude": {"id": 19, "name": "о труде", "emoji": "💼"},
    "o-trudolyubii": {"id": 20, "name": "о трудолюбии", "emoji": "🔨"},
    "o-umelyh-rukah": {"id": 21, "name": "о умелых руках", "emoji": "🤲"},
    "o-hlebe": {"id": 22, "name": "о хлебе", "emoji": "🍞"},
    "o-cheloveke": {"id": 23, "name": "о человеке", "emoji": "🧑"},
    "o-chtenii": {"id": 24, "name": "о чтении", "emoji": "📖"},
    "o-shkole": {"id": 25, "name": "о школе", "emoji": "🏫"},
    "o-yazyke": {"id": 26, "name": "о языке", "emoji": "🗣️"},
    "pro-zhivotnyh": {"id": 27, "name": "про животных", "emoji": "🐾"},
    "pro-slovo": {"id": 28, "name": "про слово", "emoji": "💬"},
    "pro-utro": {"id": 29, "name": "про утро", "emoji": "🌅"},
    "russkie": {"id": 30, "name": "русские", "emoji": "🇷🇺"},
}

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
OUTPUT = "/home/root2506/proverb_bot/data/proverbs_all.json"


async def fetch(session, url):
    try:
        async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as r:
            if r.status == 200:
                return await r.text()
    except:
        pass
    return None


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    proverbs = []
    for holder in soup.select(".holder p"):
        text = holder.get_text(separator=" ", strip=True)
        text = re.sub(r'\s+', ' ', text).strip()
        if text and len(text) > 5:
            proverbs.append(text)
    return proverbs


async def scrape_cat(session, slug, cat_id, max_pages=31):
    result = []
    for page in range(1, max_pages + 1):
        url = f"https://poslovicy.ru/{slug}/" if page == 1 else f"https://poslovicy.ru/{slug}/page/{page}/"
        html = await fetch(session, url)
        if not html:
            break
        items = parse(html)
        if not items:
            break
        result.extend(items)
        if len(items) < 5:
            break
        await asyncio.sleep(0.3)
    return result


async def main():
    seen = set()
    proverbs = []
    idx = 1

    async with aiohttp.ClientSession() as session:
        for slug, cat in CATEGORIES.items():
            print(f"{cat['name']}...", end=" ", flush=True)
            items = await scrape_cat(session, slug, cat["id"])
            added = 0
            for p in items:
                if p not in seen:
                    seen.add(p)
                    proverbs.append({"id": idx, "text": p, "category_id": cat["id"]})
                    idx += 1
                    added += 1
            print(f"+{added} (total: {len(proverbs)})")

    cats = [{"id": v["id"], "name": v["name"], "emoji": v["emoji"]} for v in CATEGORIES.values()]
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump({"categories": cats, "proverbs": proverbs}, f, ensure_ascii=False, indent=2)

    print(f"\nDone: {len(proverbs)} unique proverbs → {OUTPUT}")


if __name__ == "__main__":
    asyncio.run(main())
