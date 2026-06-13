from services.news import fetch_news
import asyncio
from cache import _cache

def test_fetch_news():
    result = asyncio.run(fetch_news("Palantir"))
    print(result)  # ← add this
    assert result.source == "newsapi"
    assert len(result.articles) > 0
    assert result.fetched_at is not None
