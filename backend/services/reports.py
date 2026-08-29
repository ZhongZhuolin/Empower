from db import async_session, ReportRecord, Company
from models import IntelligenceReport
from sqlalchemy import select
from config import HISTORY_LIMIT


# turns a company name into its id, creating the company row if it is new
async def get_or_create_company(name: str) -> int:
    async with async_session() as session:
        query = select(Company).where(Company.name == name)
        result = await session.execute(query)
        company = result.scalar_one_or_none()

        if company is not None:
            return company.id

        company = Company(name=name)
        session.add(company)
        await session.commit()
        await session.refresh(company)   # pulls back the id Postgres assigned
        return company.id


# function to write to the database of empower
async def save_report(company_id: int, report: IntelligenceReport):
    async with async_session() as session:
        record = ReportRecord(
            company_id = company_id,
            signal_score = report.signal.score,
            recommendation = report.signal.recommendation,
            reasoning = report.signal.reasoning,
            claude_summary = report.claude_summary,
        )
        session.add(record)
        await session.commit()


async def get_report_history(company_id: int, limit: int = HISTORY_LIMIT):
    async with async_session() as session:
        query = (
            select(ReportRecord)
            .where(ReportRecord.company_id == company_id)
            .order_by(ReportRecord.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(query)
        return result.scalars().all()
