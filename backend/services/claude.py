from config import settings
from anthropic import AsyncAnthropic

#logs into anthropic, calls basesettings to view claude api key
client = AsyncAnthropic(api_key = settings.ANTHROPIC_API_KEY)

async def ask_claude(company_name: str, news_text: str, wiki_text: str) -> str:

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
    5. Salary, for now pull from available online resources, for base pay for software engineering and data science, also expected intern/coop pay and benefits
    6. Recent news — structured list with each URL attached and how it ties into the company
    7. Current focus and notable recent developments
    8. Job prospects — current and future outlook for CS students
    9. Anything else relevant to a CS student considering them as an employer

    Write the overview in paragraph form. Use structured lists for products, tech stack, and news. Be direct, factual, and include your own insights where relevant.
    """

    #sends the message
    message = await client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 2000,
        #tool that allows claude to access the web to search
        tools=[
        {
            "type": "web_search_20250305",
            "name": "web_search"
        }
        ],
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    #return a full set of answers from claude
    full_response = ""
    for block in message.content:
        if block.type == "text":
            full_response += block.text
    return full_response

