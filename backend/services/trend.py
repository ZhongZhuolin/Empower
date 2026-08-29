from anthropic import AsyncAnthropic
from config import settings

def format_history(history) -> str:
    if not history:
        return "No previous reports."

    lines = []
    for record in history:
        date = record.created_at.strftime("%Y-%m-%d")
        summary = record.claude_summary[:300]
        lines.append(f"{date} - score {record.signal_score}: {summary}")

    return "\n".join(lines)

client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

async def analyze_trend(company_name: str, current_brief: str, history) -> str:
    if not history:
        return "First time researching this company. No trend yet."

    prompt = f"""No emojis or em dashes. You are tracking how a company's hiring signal has changed over time.

    Past reports for {company_name}, newest first:
    {format_history(history)}

    The newest research brief:
    {current_brief}

    In two or three sentences, say what changed since the earlier reports and why the signal moved. If nothing meaningful changed, say so plainly."""

    message = await client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = ""
    for block in message.content:
        if block.type == "text":
            text += block.text
    return text.strip()
