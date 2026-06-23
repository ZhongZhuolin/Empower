from services.claude import ask_claude
import asyncio

def test_fetch_news():
    result = asyncio.run(ask_claude("Palantir", "News", "Wiki"))
    print(result)  # ← add this
    assert result is not None
    assert len(result) > 0
