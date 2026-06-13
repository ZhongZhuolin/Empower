from cache import cache_get, cache_set
import time
from config import News_TTL
def test_cache():
    result = cache_get("palantir")
    print(result)
    assert result is None
    cache_set("palantir", "something", News_TTL, "Newsapi")
    result = cache_get("palantir")
    print(result)
    assert result is not None
    cache_set("palantir", "something", 1, "Newsapi")
    time.sleep(2)
    result = cache_get("palantir")
    print(result)
    assert result is None
