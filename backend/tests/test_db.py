import asyncio
from db import async_session, ReportRecord

async def insert_one():
    async with async_session() as session:
        record = ReportRecord(
            company_name="Google",
            signal_score=85,
            recommendation="Strong Hire",
            claude_summary="Test row to confirm inserts work.",
        )
        session.add(record)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(insert_one())
