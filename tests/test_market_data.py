from app.market_data import get_recent_bars
from app.signal import get_risk_score

bars = get_recent_bars(lookback_minutes=30)
score, price_move, volume_spike, volatility = get_risk_score(bars)

print(f"Risk score: {score}")
print(f"Price move %: {price_move:.4f}")
print(f"Volume spike ratio: {volume_spike:.4f}")
print(f"Realized volatility: {volatility:.6f}")