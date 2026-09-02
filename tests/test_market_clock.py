from alpaca.trading.client import TradingClient
from app.config import ALPACA_API_KEY, ALPACA_SECRET_KEY, PAPER_TRADING

client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=PAPER_TRADING)
clock = client.get_clock()
print("Market open:", clock.is_open)
print("Next open:", clock.next_open)
print("Next close:", clock.next_close)