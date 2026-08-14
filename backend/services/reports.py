from db import async_session, ReportRecord
from models import IntelligenceReport
from sqlalchemy import select

# function to write to the database of empower
async def save_report(company_name: str, report: IntelligenceReport):
    async with async_session() as session:
        record = ReportRecord(
            company_name = company_name,
            signal_score = report.signal.score,
            recommendation = report.signal.recommendation,
            reasoning = report.signal.reasoning, claude_summary = report.claude_summary
        )
        session.add(record)
        await session.commit()

# function to get last report
async def get_last_report(company_name: str):
    async with async_session() as session:
        query = select(ReportRecord).where(ReportRecord.company_name == company_name).order_by(ReportRecord.created_at.desc()).limit(1)
        result = await session.execute(query)
        return result.scalar_one_or_none()
