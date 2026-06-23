import asyncio
from services.news import fetch_news, format_news
from services.wiki import fetch_wiki
from services.claude import ask_claude
from models import IntelligenceReport
import datetime


#asyncio.gather runs fetch news and fetch wiki concurrently
async def fuse(company_name: str) -> IntelligenceReport:
    news_payload, wiki_payload = await asyncio.gather(
        fetch_news(company_name),
        fetch_wiki(company_name)
    )
    claude_summary = await ask_claude(company_name, format_news(news_payload.articles), wiki_payload.summary)

    #return an intelligence report object, with a news and wiki object, and source Empower
    return IntelligenceReport(
        news= news_payload,
        wiki_summary= wiki_payload,
        claude_summary= claude_summary,
        source= "Empower Fusion",
        fetched_at= datetime.datetime.now()
    )

