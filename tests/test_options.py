# tests/test_options.py
from app.options_selector import get_option_chain, find_target_put
from app.market_data import get_recent_bars

chain = get_option_chain()
print(f"Number of contracts: {len(chain)}")

bars = get_recent_bars(lookback_minutes=5)
current_price = bars[-1].close
print("Current price:", current_price)

put_symbol = find_target_put(chain, current_price=current_price)
print("Selected put:", put_symbol)