from fastapi import APIRouter
from models import ResearchRequest, IntelligenceReport
from services.fusion import fuse

router = APIRouter()

@router.post("/research", response_model=IntelligenceReport)
async def research_company(request: ResearchRequest) -> IntelligenceReport:
    # position parked for job scraping later
    return await fuse(request.company_name)
