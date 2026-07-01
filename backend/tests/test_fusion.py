from fusion import fuse
import asyncio

def test_fusion():
    result = asyncio.run(fuse("Palantir"))
    print(result.claude_summary)
    print(result.signal.score)
    print(result.signal.recommendation)
    print(result.signal.reasoning)
    assert result is not None
    assert result.source == "Empower Fusion"
    assert result.fetched_at is not None
    assert len(result.claude_summary) > 0
    assert len(result.news.articles) > 0
    assert result.wiki_summary.summary is not None
    assert result.signal.score > 0
    assert result.signal.recommendation in ["apply now", "keep watching", "pass"]
