#This file validates what the user inputs as a company and role
# as well as validates the payload from each service

from pydantic import BaseModel, Field #tool that checks if user request makes sense

import datetime
#Pydantic for parsing company and position request for string, and string length validation
class ResearchRequest(BaseModel):
    company_name: str = Field(min_length = 1, max_length = 50)
    position: str = Field(min_length = 1, max_length = 30)
#ensures each article object has proper attributes
class NewsArticle(BaseModel):
    title : str
    description : str
    url : str

#ensures newspayload has a proper list of articles
class NewsPayload(BaseModel):
    articles: list[NewsArticle]
    fetched_at: datetime.datetime
    source: str

#ensures wiki has proper attributes
class WikiPayload(BaseModel):
    summary: str
    fetched_at: datetime.datetime
    source: str

#ensures the report being sent to the user has correct information
class IntelligenceReport(BaseModel):
    news: NewsPayload
    wiki_summary: WikiPayload
    claude_summary: str
    source: str
    fetched_at: datetime.datetime
