# app/execution.py
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from app.config import ALPACA_API_KEY, ALPACA_SECRET_KEY, PAPER_TRADING

trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=PAPER_TRADING)


def place_put_order(put_symbol: str, quantity: int = 1):
    """
    Places a market order to BUY the given put option contract
    (paper trading only, per PAPER_TRADING in config).
    """
    order_request = MarketOrderRequest(
        symbol=put_symbol,
        qty=quantity,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY,
    )
    order = trading_client.submit_order(order_request)
    return order