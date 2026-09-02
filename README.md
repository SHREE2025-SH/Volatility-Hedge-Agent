# Volatility-Aware Options Hedging Agent

An autonomous agent that monitors SPY for volatility signals and automatically hedges downside risk with a protective put — executed via Alpaca's Trading API in the paper trading environment.

Built for the **Alpaca AI Trading Agents Hackathon**.

## What it does

1. **Watches** SPY using Alpaca's Market Data API (1-minute bars)
2. **Scores risk** across three signals: price move %, volume spike ratio, and realized volatility
3. **When risk crosses a threshold**, it selects a protective put option near the current price, using real live Greeks (Delta) from Alpaca's options chain to pick the nearest-the-money, nearest-expiry contract
4. **Explains its decision** in plain language using Gemini — not just "trade executed," but why the signal fired and why this specific contract was chosen
5. **Executes** the trade via Alpaca's Trading API (paper trading only)

All of this is shown live in a Streamlit dashboard.

## Why this approach

Rather than chase model sophistication (RL, custom forecasting), this agent is built around **transparency**: every decision is explainable, every number is real (not simulated), and the reasoning trail is the actual product — not an afterthought bolted onto a black-box trade.

## Architecture

```
market_data.py  → fetches live SPY bars (Alpaca Market Data API, IEX feed)
signal.py       → computes risk score from price/volume/volatility
options_selector.py → finds nearest-expiry put near target Delta (Alpaca options chain + Greeks)
reasoning.py    → Gemini-generated plain-language explanation
execution.py    → places the paper trade (Alpaca Trading API)
main.py         → wires the full pipeline together
frontend/app.py → Streamlit dashboard
```

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
ALPACA_API_KEY=your_alpaca_paper_key
ALPACA_SECRET_KEY=your_alpaca_paper_secret
GEMINI_API_KEY=your_gemini_key
```

Get Alpaca paper trading keys from [app.alpaca.markets](https://app.alpaca.markets) (API section). Get a Gemini key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

## Running it

**Command line (single run):**
```bash
python -m app.main
```

**Dashboard:**
```bash
streamlit run frontend/app.py
```

Click "Run Agent Now" to fetch live data and evaluate risk. If the risk score crosses the threshold, the dashboard shows the selected put, the reasoning, and a button to execute the trade.

## Notes

- Uses Alpaca's **IEX data feed** (free tier) — real-time SIP data requires a paid subscription
- Options orders can only be placed during **market hours** (9:30 AM–4:00 PM ET); outside that window, the agent still completes signal detection, put selection, and reasoning, and reports the execution attempt clearly
- Risk thresholds in `signal.py` are tuned for demo visibility on typical SPY intraday movement — adjust `price_move`, `volume_spike`, and `volatility` thresholds in `get_risk_score()` for production sensitivity

## Tech stack

Python, FastAPI-compatible structure, Alpaca Trading & Market Data API (`alpaca-py`), Google Gemini (`google-genai`), Streamlit