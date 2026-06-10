from fastapi import FastAPI
from pydantic import BaseModel
import requests
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

class ResearchRequest(BaseModel):
    company_name: str

@app.post("/research")
def research_company(request: ResearchRequest):

    newsapi_key = os.getenv("NEWS_API_KEY")
    news_url = "https://newsapi.org/v2/everything"

    params = {
        "q": request.company_name,
        "pageSize": 5,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": newsapi_key
    }

    news_response = requests.get(news_url, params=params)
    news_data = news_response.json()

    articles = news_data.get("articles", [])

    news_text = ""
    for article in articles:
        title = article.get("title", "")
        description = article.get("description", "")
        news_text += f"Title: {title}\nDescription: {description}\n\n"

    if not news_text.strip():
        return {"summary": "No recent news found for this company."}

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""You are a company research analyst helping a CS student evaluate companies for internships.

Here are recent articles about {request.company_name}:

{news_text}

Based on these articles, write a 3-4 sentence summary covering:
- What the company is currently focused on
- Any notable recent developments
- Anything relevant to a CS student considering them as an employer

Be direct and factual. No bullet points - write in paragraph form."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    summary = message.content[0].text

    return {
        "company": request.company_name,
        "summary": summary,
        "articles_used": len(articles)
    }
