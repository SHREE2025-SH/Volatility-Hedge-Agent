def calculate_price_move_pct(bars):
    first_close = bars[0].close
    last_close = bars[-1].close
    pct_change=((last_close - first_close) / first_close) * 100
    return pct_change

def calculate_volume_spike(bars):
    volumes = [bar.volume for bar in bars]
    avg_volume = sum(volumes[:-1]) / (len(volumes) - 1)  # Exclude the last bar for average
    last_volume = volumes[-1]
    latest_volume_spike = last_volume / avg_volume if avg_volume != 0 else float('inf')
    return latest_volume_spike

def calculate_realized_volatility(bars):
   
    closes = [bar.close for bar in bars]
    returns = [
        (closes[i] - closes[i - 1]) / closes[i - 1]
        for i in range(1, len(closes))
    ]
    mean_return = sum(returns) / len(returns)
    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
    std_dev = variance ** 0.5
    return std_dev

def get_risk_score(bars):
    price_move = calculate_price_move_pct(bars)
    volume_spike = calculate_volume_spike(bars)
    volatility = calculate_realized_volatility(bars)

    score = 0
    if price_move > 0.5:
        score += 1

    if volume_spike > 1.3:
        score += 1

    if volatility > 0.001:
        score += 1

    return score, price_move, volume_spike, volatility


