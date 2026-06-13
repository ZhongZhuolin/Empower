import time
import httpx
from models import NewsArticle, NewsPayload
from cache import cache_set, cache_get
from config import News_TTL, settings
import datetime
#calls an newsapi.org to search through news articles related to requested company
#declares an async function that allows for pausing to let other functions to run
#httpx
async def fetch_news(company_name: str) -> NewsPayload:

    cached = cache_get(company_name)
    if cached is not None:
        articles, _ = cached
        return NewsPayload(
        articles = articles,
        fetched_at = datetime.datetime.now(),
        source = "newsapi"
    )

    #searches for everything, for more info look at newsapi api docs
    news_url = "https://newsapi.org/v2/everything"

    params = {
        "q" : company_name,
        "pageSize" : 10,
        "sortBy": "relevancy",
        "language": "en",
        "apiKey" : settings.NEWS_API_KEY
    }

    #async web request, shortcut to clode client even if the response crashes and prevent open leaks
    async with httpx.AsyncClient() as client:
        response = await client.get(news_url, params=params)

    #formats as json/dictionary with key = "articles"
    raw_articles = response.json().get("articles", [])

    articles = []
    for article in raw_articles:
        news_article = NewsArticle(title=article.get("title", ""), description=article.get("description", ""), url=article.get("url", ""))
        articles.append(news_article)

    cache_set(company_name, articles, News_TTL)

    return NewsPayload(
        articles = articles,
        fetched_at = datetime.datetime.now(),
        source = "newsapi"
    )
