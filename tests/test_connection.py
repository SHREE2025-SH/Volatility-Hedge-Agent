from alpaca.trading.client import TradingClient
from app.config import ALPACA_API_KEY, ALPACA_SECRET_KEY, PAPER_TRADING

trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=PAPER_TRADING)
account = trading_client.get_account()

print(f"Account status: {account.status}")
print(f"Buying power: ${account.buying_power}")
print(f"Options trading level: {account.options_trading_level}")