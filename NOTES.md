# My Notes

## config.py
- Loads secrets from .env (API keys) — never commit .env to GitHub
- TICKER = 'SPY': which stock we watch/trade options on. SPY chosen for high liquidity/reliable options chains
- Other liquid ticker options I could swap in later: QQQ (Nasdaq-100), AAPL, TSLA (more volatile, could show more signal activity), IWM (small-cap index)
- PAPER_TRADE = True: Alpaca's simulated trading mode — fake money, real market data, safe for hackathon

## Debugging notes
- Hit "must supply a method of authentication" error — turned out I'd accidentally typed placeholder text into os.getenv() instead of the actual variable name string
- Learned: os.getenv("VAR_NAME") takes the variable's NAME as a string, never the real value — the real value only lives in .env


## market_data.py — debugging notes
- Bug: used bars(TICKER) instead of bars[TICKER] — BarSet is a dict-like object, indexed with [], not called with ()
- Fixed, now returns real minute-by-minute bars: timestamp, close price, volume

## signal.py — three functions, all tested together
- calculate_price_move_pct: % change from first to last bar in window
- calculate_volume_spike: latest bar volume vs avg of rest of window
- calculate_realized_volatility: std dev of minute-to-minute returns
- All three confirmed working against live SPY data


## market_data.py — debugging notes
- Market was closed (weekend) when testing — "no key SPY was found" error
- Free Alpaca tier can't query recent SIP data — switched to feed=DataFeed.IEX
- Widened lookback to 5 days back, then sliced last N bars, to always land on real trading data

## options_selector.py — debugging notes
- Scanning all 13,514 contracts one-by-one was too slow (25+ min, no result)
- Fixed by: (1) narrowing to a single nearest expiry date instead of a 45-day range, (2) batching the Greeks request for all candidates in one API call instead of looping
- Selected SPY260902P00765000 — a real put near our target delta range


## reasoning.py — debugging notes
- google.generativeai package is fully deprecated — switched to the new google-genai SDK
- gemini-1.5-flash retired, then gemini-2.5-flash also retired for new users
- API itself told us the correct current model: gemini-3.6-flash — used that
- New SDK pattern: genai.Client(api_key=...) then client.models.generate_content(model=..., contents=...)


## execution.py — debugging notes
- Order submission correctly rejected with "options market orders are only allowed during market hours" — expected behavior since Alpaca paper markets follow real NYSE hours
- Confirms the order request is correctly formatted and authenticated
- Need to re-test with a live successful execution once market reopens (Sep 1, 7:00 PM IST) — required for demo video proof