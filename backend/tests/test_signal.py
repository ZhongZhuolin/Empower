from services.signal import score_signals
from services.claude import ask_claude
import asyncio

#runs the claude api prompt to retrive a brief, then
def test_signal():
    result = asyncio.run(ask_claude("Palantir", "News", "Wiki"))
    score =  asyncio.run(score_signals("Palantir", result))
    print(score.score)
    print(score.recommendation)
    print(score.reasoning)
    assert score is not None
