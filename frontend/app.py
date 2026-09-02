# frontend/app.py
"""
Volatility-Aware Options Hedging Agent — Dashboard

Run with:
    streamlit run frontend/app.py
"""

import streamlit as st
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config import TICKER
from app.market_data import get_recent_bars
from app.signal import get_risk_score
from app.options_selector import get_option_chain, find_target_put
from app.reasoning import explain_decision
from app.execution import place_put_order

# ---------- Page config ----------
st.set_page_config(page_title="Volatility Hedge Agent", page_icon="⚡", layout="centered")

# ---------- Theme: black / white / yellow (Alpaca-style) ----------
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0a0a0a;
            color: #f5f5f5;
        }
        h1, h2, h3 {
            color: #ffffff !important;
        }
        .accent {
            color: #FFD400;
        }
        .metric-card {
            background-color: #141414;
            border: 1px solid #262626;
            border-radius: 10px;
            padding: 18px 20px;
            margin-bottom: 10px;
        }
        .metric-label {
            color: #9a9a9a;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }
        .metric-value {
            color: #ffffff;
            font-size: 24px;
            font-weight: 700;
        }
        .score-card {
            border-radius: 10px;
            padding: 20px 24px;
            margin: 20px 0;
        }
        .score-triggered {
            background-color: #1a1704;
            border: 1px solid #FFD400;
        }
        .score-calm {
            background-color: #141414;
            border: 1px solid #262626;
        }
        .score-label {
            color: #9a9a9a;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .score-value {
            font-size: 28px;
            font-weight: 800;
            margin-top: 4px;
        }
        .put-badge {
            display: inline-block;
            background-color: #1a1704;
            border: 1px solid #FFD400;
            color: #FFD400;
            padding: 8px 14px;
            border-radius: 6px;
            font-family: monospace;
            font-size: 15px;
        }
        .reasoning-box {
            background-color: #141414;
            border-left: 3px solid #FFD400;
            border-radius: 6px;
            padding: 16px 20px;
            color: #d4d4d4;
            line-height: 1.6;
            margin-top: 10px;
        }
        div.stButton > button {
            background-color: #FFD400;
            color: #0a0a0a;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
        }
        div.stButton > button:hover {
            background-color: #e6bf00;
            color: #0a0a0a;
        }
        .stCaption {
            color: #9a9a9a !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown(f"# Volatility Hedge <span class='accent'>Agent</span>", unsafe_allow_html=True)
st.caption(f"Watching **{TICKER}** · Autonomous protective-put hedging on Alpaca Paper Trading")
st.write("")

# ---------- Session state ----------
if "result" not in st.session_state:
    st.session_state.result = None

# ---------- Run button ----------
run_clicked = st.button("Run Agent Now", type="primary")

if run_clicked:
    with st.spinner("Fetching market data..."):
        bars = get_recent_bars(lookback_minutes=30)
        current_price = bars[-1].close
        score, price_move, volume_spike, volatility = get_risk_score(bars)

    # Build simple price/volume series for charting
    chart_prices = [bar.close for bar in bars]
    chart_volumes = [bar.volume for bar in bars]
    chart_times = [bar.timestamp.strftime("%H:%M") for bar in bars]

    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "current_price": current_price,
        "score": score,
        "price_move": price_move,
        "volume_spike": volume_spike,
        "volatility": volatility,
        "put_symbol": None,
        "explanation": None,
        "chart_prices": chart_prices,
        "chart_volumes": chart_volumes,
        "chart_times": chart_times,
    }

    if score >= 1:
        with st.spinner("Selecting protective put..."):
            chain = get_option_chain()
            put_symbol = find_target_put(chain, current_price=current_price)
        result["put_symbol"] = put_symbol

        if put_symbol:
            with st.spinner("Generating reasoning..."):
                explanation = explain_decision(
                    ticker=TICKER,
                    score=score,
                    price_move=price_move,
                    volume_spike=volume_spike,
                    volatility=volatility,
                    put_symbol=put_symbol,
                )
            result["explanation"] = explanation

    st.session_state.result = result

# ---------- Display last result ----------
result = st.session_state.result

if result:
    st.caption(f"Last run: {result['timestamp']}")

    c1, c2, c3, c4 = st.columns(4)
    for col, label, value in zip(
        [c1, c2, c3, c4],
        ["Current Price", "Price Move", "Volume Spike", "Volatility"],
        [
            f"${result['current_price']:.2f}",
            f"{result['price_move']:.3f}%",
            f"{result['volume_spike']:.2f}x",
            f"{result['volatility']:.5f}",
        ],
    ):
        with col:
            st.markdown(
                f"""<div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    # Price + volume charts
    import pandas as pd

    st.markdown("#### Price Movement (last 30 min)")
    price_df = pd.DataFrame({"Price": result["chart_prices"]}, index=result["chart_times"])
    st.line_chart(price_df, color="#FFD400", height=220)

    st.markdown("#### Volume")
    volume_df = pd.DataFrame({"Volume": result["chart_volumes"]}, index=result["chart_times"])
    st.bar_chart(volume_df, color="#666666", height=140)

    score = result["score"]
    score_class = "score-triggered" if score >= 1 else "score-calm"
    score_text = "Hedge Triggered" if score >= 1 else "No Action Needed"
    score_color = "#FFD400" if score >= 1 else "#ffffff"
    st.markdown(
        f"""<div class="score-card {score_class}">
            <div class="score-label">Risk Score</div>
            <div class="score-value" style="color:{score_color}">{score} / 3 — {score_text}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    if result["put_symbol"]:
        st.markdown("#### Selected Hedge")
        st.markdown(f"<span class='put-badge'>{result['put_symbol']}</span>", unsafe_allow_html=True)

        st.markdown("#### Agent Reasoning")
        st.markdown(f"<div class='reasoning-box'>{result['explanation']}</div>", unsafe_allow_html=True)

        st.write("")
        if st.button("Execute Trade (Paper)"):
            with st.spinner("Placing order..."):
                try:
                    order = place_put_order(result["put_symbol"], quantity=1)
                    st.success(f"Order placed successfully — ID: {order.id} | Status: {order.status}")
                except Exception as e:
                    st.warning(f"Order could not be placed: {e}")
    elif score >= 1:
        st.warning("Risk threshold crossed, but no suitable put option was found.")
else:
    st.info("Click **Run Agent Now** to fetch live market data and evaluate risk.")