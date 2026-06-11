#imports
from fastapi import FastAPI #Framework for processing user requests, returns json
import requests #allows python to make web requests
import anthropic #official tool for claude
import os #allows python to talk to operating system, like .env
import datetime

#creates an object of class fastapi that listens for web requests
app = FastAPI()

#calls level.fyi api to search for company positions and salary
# def fetch_salary(company_name: str, role: str) -> list:
#     levels_url = ""
#     params = {

#     }

#     levels_response = requests.get(levels_url, params = params)

#     levels_data = levels_response.json()

#     return levels_data.get(role, [])
#work on this ^^

#formats levels.fyi dictionary into structured text for claude to parse
# def format_roles(roles: list) -> str:
#     roles_text = ""
#     #loops through positions and appends title and salary to roles_text
#     for position in roles:
#         title = position.get("title", "")
#         salary = position.get("wage", "")
#         url = position.get("url", "")
#         roles_text += f"Title: {title}\nSalary: {description}\nURL:{url}\n\n"

#     return roles_text
#work on this ^^


def ask_claude(company_name: str, news_text: str, wiki_text: str) -> str:
    #logs into anthropic, calls basesettings to view claude api key
    client = anthropic.Anthropic(api_key = settings.ANTHROPIC_API_KEY)

    #message that is sent to claude

    prompt = f"""You are a company research analyst helping a CS student evaluate companies for internships.

    Company background (Wikipedia):
    {wiki_text}

    Recent news:
    {news_text}

    Based on the above and your own knowledge about {company_name}, write a structured research brief covering:

    1. Company overview — what the company is and does
    2. How prestigious it is for tech, and its ranking amongst similar
    sectors, startups, financial tech companies, and big tech
    3. Main products and software — detailed list
    4. Tech stack — detailed list
    5. Recent news — structured list with each URL attached and how it ties into the company
    6. Current focus and notable recent developments
    7. Job prospects — current and future outlook for CS students
    8. Anything else relevant to a CS student considering them as an employer

    Write the overview in paragraph form. Use structured lists for products, tech stack, and news. Be direct, factual, and include your own insights where relevant.
    """

    #sends the message
    message = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 700,
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
    wiki_summary = fetch_wiki(request.company_name)

    brief = ask_claude(request.company_name, news_text, wiki_summary)

    return{
        "Company": request.company_name,
        "Summary": summary,
        "recent_news": recent_news,
        "Articles Used": len(articles)
    }





