from sqlalchemy.ext.asyncio import create_async_engine
from config import settings
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func
import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker

engine = create_async_engine(settings.DATABASE_URL)

class Base(DeclarativeBase):
    pass

class ReportRecord(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    company_name  = Column(String, nullable=False)
    signal_score = Column(Integer, nullable=False)
    recommendation = Column(String, nullable=False)
    claude_summary = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

async_session = async_sessionmaker(engine)
