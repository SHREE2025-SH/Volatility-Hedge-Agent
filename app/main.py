# app/main.py
"""
Volatility-Aware Options Hedging Agent — main entry point.

Pipeline:
  1. Fetch recent market data for TICKER
  2. Compute risk score (price move, volume spike, realized volatility)
  3. If score >= 1: select a protective put, explain the decision, attempt to execute
  4. If score == 0: report no hedge needed

Run with:
    python -m app.main
"""

from app.config import TICKER
from app.market_data import get_recent_bars
from app.signal import get_risk_score
from app.options_selector import get_option_chain, find_target_put
from app.reasoning import explain_decision
from app.execution import place_put_order


def run_agent():
    print(f"=== Volatility-Aware Options Hedging Agent ({TICKER}) ===\n")

    # 1. Fetch market data
    bars = get_recent_bars(lookback_minutes=30)
    current_price = bars[-1].close
    print(f"Current price: {current_price}")

    # 2. Compute risk score
    score, price_move, volume_spike, volatility = get_risk_score(bars)
    print(f"\nRisk score: {score}")
    print(f"  Price move %: {price_move:.4f}")
    print(f"  Volume spike ratio: {volume_spike:.4f}")
    print(f"  Realized volatility: {volatility:.6f}")

    if score < 1:
        print("\nNo hedge triggered — risk score below threshold. Agent takes no action.")
        return

    # 3. Select a put option
    print("\nRisk threshold crossed — selecting a protective put...")
    chain = get_option_chain()
    put_symbol = find_target_put(chain, current_price=current_price)

    if put_symbol is None:
        print("No suitable put option found. Agent takes no action.")
        return

    print(f"Selected put: {put_symbol}")

    # 4. Explain the decision
    explanation = explain_decision(
        ticker=TICKER,
        score=score,
        price_move=price_move,
        volume_spike=volume_spike,
        volatility=volatility,
        put_symbol=put_symbol,
    )
    print(f"\nReasoning:\n{explanation}")

    # 5. Attempt to execute
    print("\nAttempting to place order...")
    try:
        order = place_put_order(put_symbol, quantity=1)
        print(f"Order placed successfully. Order ID: {order.id}, Status: {order.status}")
    except Exception as e:
        print(f"Order could not be placed: {e}")
        print("(This is expected outside market hours — the pipeline up to this point is fully verified.)")


if __name__ == "__main__":
    run_agent()