import asyncio
from services.news import fetch_news, format_news
from services.wiki import fetch_wiki
from services.claude import ask_claude
from models import IntelligenceReport
import datetime
from services.scoring import score_signals_stable
from services.reports import save_report, get_report_history, get_or_create_company
from services.trend import analyze_trend
from cache import cache_get, cache_set
from config import Report_TTL

#asyncio.gather runs fetch news and fetch wiki concurrently
async def fuse(company_name: str) -> IntelligenceReport:
    cached = cache_get(company_name)
    if cached is not None:
        report, source = cached
        return report
    news_payload, wiki_payload = await asyncio.gather(
        fetch_news(company_name),
        fetch_wiki(company_name)
    )
    claude_summary = await ask_claude(company_name, format_news(news_payload.articles), wiki_payload.summary)

    signal = await score_signals_stable(company_name, claude_summary)

    company_id = await get_or_create_company(company_name)
    history = await get_report_history(company_id)
    previous_score = history[0].signal_score if history else None
    trend = await analyze_trend(company_name, claude_summary, history)

    report = IntelligenceReport(
        news = news_payload,
        wiki_summary = wiki_payload,
        claude_summary = claude_summary,
        source = "Empower Fusion",
        signal = signal,
        fetched_at = datetime.datetime.now(),
        previous_score = previous_score,
        trend = trend,
    )

    await save_report(company_id, report)
    cache_set(company_name, report, Report_TTL, "cache")
    return report


