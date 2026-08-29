# signals the brief that claude returns
import json
from anthropic import AsyncAnthropic
from config import settings
from models import SignalScore
import asyncio
import statistics

client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

async def score_signals(company_name: str, brief: str) -> SignalScore:
    prompt = f""" No EMOJIS or emdashes!!! You are a recruiting-signal analyst. Based on the research brief below for {company_name}, rate how strong a signal it is for a CS student to apply RIGHT NOW.

Brief:
{brief}

Scale:
1-3 = low signal, not actively hiring
4-6 = moderate, worth watching
7-9 = high signal, actively growing, apply now
10 = exceptional, rare, major hiring push

Return ONLY a JSON object, no markdown, exactly this shape:
{{"score": <int 1-10>, "recommendation": "<apply now | keep watching | pass>", "reasoning": "<one or two sentences>"}}"""

    message = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = ""
    for block in message.content:
        if block.type == "text":
            text += block.text

    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        return SignalScore(**json.loads(text))
    except (json.JSONDecodeError, ValueError, TypeError):
        return SignalScore(score=0, recommendation="unknown", reasoning="Could not parse signal score.")

async def score_signals_stable(company_name: str, brief: str, samples: int = 3) -> SignalScore:
    # start 3 scoring jobs
    jobs = []
    for i in range(samples):
        jobs.append(score_signals(company_name, brief))

    # run them all at the same time, wait for all 3
    results = await asyncio.gather(*jobs)

    # pull just the numbers out
    scores = []
    for r in results:
        scores.append(r.score)

    median = int(statistics.median(scores))

    # find the result whose score is closest to the median
    closest = results[0]
    for r in results:
        if abs(r.score - median) < abs(closest.score - median):
            closest = r

    return SignalScore(
        score=median,
        recommendation=closest.recommendation,
        reasoning=closest.reasoning,
    )
