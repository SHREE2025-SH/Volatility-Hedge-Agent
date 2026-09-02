from app.reasoning import explain_decision

explanation = explain_decision(
    ticker="SPY",
    score=1,
    price_move=0.6,
    volume_spike=1.8,
    volatility=0.0021,
    put_symbol="SPY260902P00765000",
)
print(explanation)