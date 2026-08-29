from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UniqueConstraint, func
from config import settings

# the engine owns the connection pool - made once, reused for every query
engine = create_async_engine(settings.DATABASE_URL)

# a factory - call async_session() to get a fresh session per request
async_session = async_sessionmaker(engine)

# every class below inherits from Base, which collects them into Base.metadata
Base = declarative_base()


# ---------- tables nothing else depends on ----------

class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True)
    email           = Column(String, nullable=False, unique=True)
    discord_webhook = Column(String)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())


class Company(Base):
    __tablename__ = "companies"

    id               = Column(Integer, primary_key=True)
    name             = Column(String, nullable=False, unique=True)
    greenhouse_board = Column(String)
    created_at       = Column(DateTime(timezone=True), server_default=func.now())


# ---------- tables that point at the ones above ----------

class Watch(Base):
    """One row = one user watching one company for one role."""
    __tablename__ = "watches"

    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    role       = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # stops the same user watching the same company for the same role twice
    __table_args__ = (UniqueConstraint("user_id", "company_id", "role"),)


class JobPosting(Base):
    """Every job we have ever seen. first_seen is when WE noticed it."""
    __tablename__ = "job_postings"

    id          = Column(Integer, primary_key=True)
    company_id  = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    external_id = Column(String, nullable=False)
    title       = Column(String, nullable=False)
    url         = Column(String, nullable=False)
    first_seen  = Column(DateTime(timezone=True), server_default=func.now())

    # greenhouse ids are only unique within one board, so scope it to the company.
    # inserts that fail this check are jobs we already knew about.
    __table_args__ = (UniqueConstraint("company_id", "external_id"),)


class ReportRecord(Base):
    """One research run. No unique constraint - duplicates ARE the history."""
    __tablename__ = "reports"

    id             = Column(Integer, primary_key=True)
    company_id     = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    signal_score   = Column(Integer, nullable=False)
    recommendation = Column(String, nullable=False)
    claude_summary = Column(String, nullable=False)
    reasoning      = Column(String, nullable=False)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())
