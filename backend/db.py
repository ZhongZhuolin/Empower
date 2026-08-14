from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, func
from config import settings

engine = create_async_engine(settings.DATABASE_URL)
async_session = async_sessionmaker(engine)

Base = declarative_base()

class ReportRecord(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    company_name  = Column(String, nullable=False)
    signal_score = Column(Integer, nullable=False)
    recommendation = Column(String, nullable=False)
    claude_summary = Column(String, nullable=False)
    reasoning = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


