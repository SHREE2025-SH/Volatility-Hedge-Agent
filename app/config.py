from dotenv import load_dotenv
import os
import streamlit as st
for key in ["ALPACA_API_KEY", "ALPACA_SECRET_KEY", "GEMINI_API_KEY"]:
    if key in st.secrets:
        os.environ[key] = st.secrets[key]
load_dotenv()



ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

TICKER= 'SPY'
PAPER_TRADING = True