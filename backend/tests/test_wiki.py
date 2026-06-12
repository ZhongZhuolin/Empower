from services.wiki import fetch_wiki
import asyncio
# test the async function fetch_wiki, works!
def test_fetch_wiki():
    result = asyncio.run(fetch_wiki("BAE Systems"))
    print(result)
    assert len(result.summary) > 0
    assert result.fetched_at is not None


