import asyncio
from services.news import fetch_news, format_news
from services.wiki import fetch_wiki
from services.claude import ask_claude
from models import IntelligenceReport
import datetime
from services.scoring import score_signals
from services.reports import save_report, get_last_report


#asyncio.gather runs fetch news and fetch wiki concurrently
async def fuse(company_name: str) -> IntelligenceReport:
    news_payload, wiki_payload = await asyncio.gather(
        fetch_news(company_name),
        fetch_wiki(company_name)
    )
    claude_summary = await ask_claude(company_name, format_news(news_payload.articles), wiki_payload.summary)
    signal = await score_signals(company_name, claude_summary)
    #return an intelligence report object, with a news and wiki object, and source Empower
    last_report = await get_last_report(company_name)
    previous_score = last_report.signal_score if last_report else None
    report =  IntelligenceReport(
        news = news_payload,
        wiki_summary = wiki_payload,
        claude_summary = claude_summary,
        source = "Empower Fusion",
        signal = signal,
        fetched_at = datetime.datetime.now(),
        previous_score = previous_score
    )
    await save_report(company_name, report)
    return report


