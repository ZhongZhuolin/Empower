#File for fetching news
import httpx
from models import NewsArticle, NewsPayload
from cache import cache_set, cache_get
from config import News_TTL, settings
import datetime
from fastapi import HTTPException
#calls an newsapi.org to search through news articles related to requested company
#declares an async function that allows for pausing to let other functions to run
#httpx
async def fetch_news(company_name: str) -> NewsPayload:
    #get the key news:company to prevent naming conflicts
    cached = cache_get(f"news:{company_name}")
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
        "pageSize" : 4,
        "sortBy": "relevancy",
        "language": "en",
        "apiKey" : settings.NEWS_API_KEY
    }

    #async web request, shortcut to clode client even if the response crashes and prevent open leaks
    async with httpx.AsyncClient() as client:
        response = await client.get(news_url, params=params)

    #formats as json/dictionary with key = "articles"
    raw_articles = response.json().get("articles", [])
    #print(raw_articles) //can uncomment to view json
    articles = []
    for article in raw_articles:
        if article.get("description") is None:
            continue
        news_article = NewsArticle(title=article.get("title", ""),
        description=article.get("description", ""),
        url=article.get("url", "")
        )
        articles.append(news_article)
    #moved here so we can see if the articles have descriptions first and isn't linked to consent walls
    if not articles:
        raise HTTPException(status_code=404, detail="No News articles found for this company")
        
    #set the key to be news:company to prevent naming conflicts
    cache_set(f"news:{company_name}", articles, News_TTL)

    return NewsPayload(
        articles = articles,
        fetched_at = datetime.datetime.now(),
        source = "newsapi"
    )

#formats news with title, description, and url
def format_news(articles: list) -> str:
    news_text = ""
    if not articles:
        return "No articles found for this company"
    for article in articles:
        article_title = article.title
        article_description = article.description
        article_url = article.url
        news_text += f"Title:{article_title}\nDescription:{article_description}\nURL:{article_url}\n\n"

    return news_text
