# app/market_data.py
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed
from datetime import datetime, timedelta, timezone
from app.config import ALPACA_API_KEY, ALPACA_SECRET_KEY, TICKER

data_client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)


def get_recent_bars(lookback_minutes: int = 30):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=5)

    request = StockBarsRequest(
        symbol_or_symbols=TICKER,
        timeframe=TimeFrame.Minute,
        start=start_time,
        end=end_time,
        limit=lookback_minutes,
        feed=DataFeed.IEX,
    )
    bars = data_client.get_stock_bars(request)
    return bars[TICKER][-lookback_minutes:]