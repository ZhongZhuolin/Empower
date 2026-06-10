#imports
from fastapi import FastAPI #Framework for processing user requests, returns json
from pydantic import BaseModel #tool that checks is user request makes sense
from pydantic_settings import BaseSettings, SettingsConfigDict #tool that makes sure api keys are valid strings
import requests #allows python to make web requests
import anthropic #official tool for claude
import os #allows python to talk to operating system, like .env
import datetime
from pathlib import Path

#creates an object of class fastapi that listens for web requests
app = FastAPI()

#Pydantic for parsing company and position request for string validation
class ResearchRequest(BaseModel):
    company_name: str
    position: str

#Pydantic for parsing api keys and string validation
class Settings(BaseSettings):
    NEWS_API_KEY: str
    ANTHROPIC_API_KEY: str
    #since this finds a relative path, i used pathlib to find a path to env in the same folder as this file main.py
    model_config = SettingsConfigDict(env_file= Path(__file__).parent / ".env")


# BaseSettings object which holds:
# - ANTHROPIC_API_KEY
# - NEWS_API_KEY
# - WIKI_API_KEY
# - LEVELS_FYI_API_KEY
settings = Settings()

#calls an newsapi.org to search through news articles related to requested company
def fetch_news(company_name: str) -> list:

    #searches for everything, for more info look at newsapi api docs
    news_url = "https://newsapi.org/v2/everything"

    params = {
        "q" : company_name,
        "pageSize" : 10,
        "sortBy": "relevancy",
        "language": "en",
        "apiKey" : settings.NEWS_API_KEY
    }

    #makes web request
    news_response = requests.get(news_url, params = params)

    #formats as json/dictionary with key = "articles"
    news_data = news_response.json()

    #get article objects, if nothing return empty list
    return news_data.get("articles", [])

#calls level.fyi api to search for company positions and salary
def fetch_salary(company_name: str, role: str) -> list:
    levels_url = ""
    params = {

    }

    levels_response = requests.get(levels_url, params = params)

    levels_data = levels_response.json()

    return levels_data.get(role, [])
#work on this ^^

#wikipedia summary still deciding whether to return string or list
def fetch_wiki(company_name: str) -> str:

    #searches for everything, for more info look at newsapi api docs
    wiki_url = ""

    params = {
        "q" : company_name,
        "language": "en",
        "apiKey" : settings.WIKI_API_KEY
    }

    #makes web request
    wiki_response = requests.get(wiki_url, params = params)

    #formats as json/dictionary with key = "articles"
    wiki_data = wiki_response.json()

    #get article objects, if nothing return empty list
    return wiki_data.get("information", [])
#work on this ^^

#formats article dictionary into structured text for claude to parse
def format_articles(articles: list) -> str:
    news_text = ""
    #loops through articles and appends title and description to news_text
    for article in articles:
        title = article.get("title", "")
        description = article.get("description", "")
        url = article.get("url", "")
        news_text += f"Title: {title}\nDescription: {description}\nURL:{url}\n\n"

    return news_text

#formats levels.fyi dictionary into structured text for claude to parse
def format_roles(roles: list) -> str:
    roles_text = ""
    #loops through positions and appends title and salary to roles_text
    for position in roles:
        title = position.get("title", "")
        salary = position.get("wage", "")
        url = position.get("url", "")
        roles_text += f"Title: {title}\nSalary: {description}\nURL:{url}\n\n"

    return roles_text
#work on this ^^

def ask_claude_sum(company_name: str, company_sum: str) -> str:
    #logs into anthropic, calls basesettings to view claude api key
    client = anthropic.Anthropic(api_key = settings.ANTHROPIC_API_KEY)

    #message that is sent to claude

    prompt = f"""You are a company research analyst helping a CS student evaluate tech companies for internships.

    Using your own knowledge about {company_name}, along with this wikipedia summary {company_sum},
    write two short paragraphs:

    Paragraph 1 - What they do: What does this company build or sell?
    Who are their customers? What are they known for? How Prestigious are they in the tech indurstry
    and where do they rank compared to similary industries and big tech, and finance.

    Paragraph 2 - As an employer: What is the culture like? What kind of CS student thrives there?
    How selective are they?

    Be direct and specific. No bullet points. If you are not confident about
    something, say so rather than guessing."""

    #sends the message
    message = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 300,
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    #claude usually returns one block, so i used [0] as a shortcut
    return message.content[0].text


def ask_claude(company_name: str, news_text: str) -> str:
    #logs into anthropic, calls basesettings to view claude api key
    client = anthropic.Anthropic(api_key = settings.ANTHROPIC_API_KEY)

    #message that is sent to claude

    prompt = f"""
    You are a company research analyst helping a CS student evaluate companies for interns
    here are the recent articles about {company_name}:
    {news_text}
    Based on these articles list, write a 3-4 sentence summary covering:
    - A summary of recent news relevent for a jobseeker or interview
    - What the company is currently focused on
    - Any notable recent developements
    - anything relevent to a cs student considering them as an employer

    Be direct and factual. No bullet points - write in paragraph form."""

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
def research_company(request: ResearchRequest) -> dict:
    #get a list of articles, return empty if nothing is returned
    articles = fetch_news(request.company_name)
    if not articles:
        return "No recent news was found on this company"

    #get a string of articles,
    news_text = format_articles(articles)
    sum = fetch_wiki(request.company_name)

    summary = ask_claude_sum(request.company_name, sum)
    recent_news = ask_claude(request.company_name, news_text)

    return{
        "Company": request.company_name,
        "Summary": summary,
        "recent_news": recent_news,
        "Articles Used": len(articles)
    }





