# app/reasoning.py
from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-3.6-flash"

REASONING_PROMPT_TEMPLATE = """You are a risk-hedging assistant for an options trading agent.

The agent detected the following signals for {ticker}:
- Price move over the window: {price_move:.3f}%
- Volume spike ratio: {volume_spike:.2f}x normal
- Realized volatility: {volatility:.6f}
- Total risk score: {score} (out of 3)

Based on this, the agent selected this protective put option to hedge downside risk:
{put_symbol}

Write a short (2-3 sentence) plain-language explanation for a trader reviewing this decision:
1. Why the risk score triggered a hedge (reference the specific signal(s) that crossed their threshold)
2. Why this specific put option is a reasonable choice

Keep it concise and factual, no hype language.
"""


def explain_decision(ticker, score, price_move, volume_spike, volatility, put_symbol):
    prompt = REASONING_PROMPT_TEMPLATE.format(
        ticker=ticker,
        price_move=price_move,
        volume_spike=volume_spike,
        volatility=volatility,
        score=score,
        put_symbol=put_symbol,
    )
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text.strip()
