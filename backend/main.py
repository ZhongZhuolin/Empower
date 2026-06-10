#imports
from fastapi import FastAPI #Framework for processing user requests, returns json
from pydantic import BaseModel #tool that checks is user request makes sense
from pydantic_settings import BaseSettings, SettingsConfigDict
import requests #allows python to make web requests
import anthropic #official tool for claude
import os #allows python to talk to operating system, like .env
import datetime
from pathlib import Path

#creates an object of class fastapi that listens for web requests
app = FastAPI()

#Pydantic handles error codes if user doesnt put in string
class ResearchRequest(BaseModel):
    company_name: str

#Pydantic for parsing api key
class Settings(BaseSettings):
    NEWS_API_KEY: str
    ANTHROPIC_API_KEY: str
    #since this finds a relative path, i used pathlib to find a path to env in the same folder as this file main.py
    model_config = SettingsConfigDict(env_file= Path(__file__).parent / ".env")

settings = Settings()

#calls an newsapi.org to search through news articles related to requested company
def fetch_news(company_name: str):

    #searches for everything, for more info look at newsapi api docs
    news_url = "https://newsapi.org/v2/everything"
    year_ago = (datetime.date.today() - datetime.timedelta(days = 365)).isoformat()
    params = {
        "q" : company_name,
        "pageSize" : 5,
        "sortBy": "publishedAt",
        "language": "en",

        "apiKey" : settings.NEWS_API_KEY
    }

    #makes web request
    news_response = requests.get(news_url, params = params)

    #formats as json/dictionary with key = "articles"
    news_data = news_response.json()

    #get article objects, if nothing return empty list
    return news_data.get("articles", [])
#work on this ^^

#formats a dictionary into structured text for claude to parse
def format_articles(articles: list):
    news_text = ""
    #loops through articles and appends title and description to news_text
    for article in articles:
        title = article.get("title", "")
        description = article.get("description", "")
        news_text += f"Title: {title}\nDescription: {description}\n\n"

    return news_text


def ask_claude(company_name: str, news_text: str):
    #logs into anthropic, calls basesettings to view claude api key
    client = anthropic.Anthropic(api_key = settings.ANTHROPIC_API_KEY)

    #message that is sent to claude

    prompt = f"""
    You are a company research analyst helping a CS student evaluate companies for interns
    here are the recent articles about {company_name}:

    {news_text}

    Based on these articles, write a 3-4 sentence summary covering:
    - What the company is currently focused on
    - Any notable recent developements
    -anything relevent to a cs student considering them as an employer

    Be direct and factual. No bullet points - write in paragraph form.
"""

    #sends the message
    message = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 400,
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    #claude usually returns one block, so i used [0] as a shortcut
    return message.content[0].text

#phone extension routes when someone sends a post request, call the function wrapped under it
@app.post("/research")
def research_company(request: ResearchRequest):
    articles = fetch_news(request.company_name)

    if not articles:
        return "No recent news was found on this company"

    news_text = format_articles(articles)
    summary = ask_claude(request.company_name, news_text)

    return{
        "Company": request.company_name,
        "Summary": summary,
        "Articles Used": len(articles)
    }





