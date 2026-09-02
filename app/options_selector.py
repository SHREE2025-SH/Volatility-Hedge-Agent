# app/options_selector.py
import re
from alpaca.data.historical.option import OptionHistoricalDataClient
from alpaca.data.requests import OptionChainRequest, OptionSnapshotRequest
from app.config import ALPACA_API_KEY, ALPACA_SECRET_KEY, TICKER

option_client = OptionHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)


def get_option_chain():
    """
    Fetches the full option chain (contracts) for our ticker.
    """
    request = OptionChainRequest(underlying_symbol=TICKER)
    chain = option_client.get_option_chain(request)
    return chain


def get_snapshot(symbol: str):
    """
    Fetches the live snapshot (including Greeks/IV) for one specific
    option contract symbol.
    """
    request = OptionSnapshotRequest(symbol_or_symbols=symbol)
    snapshot = option_client.get_option_snapshot(request)
    return snapshot[symbol]


def find_target_put(chain, target_delta_low: float = -0.40, target_delta_high: float = -0.30, current_price: float = None):
    """
    Finds the nearest upcoming expiry date, filters to PUT contracts at
    that expiry within a tight strike range, then fetches Greeks for
    that whole shortlist in ONE batched API call (not one-by-one).
    """
    from datetime import datetime, timedelta

    target_mid = (target_delta_low + target_delta_high) / 2
    pattern = re.compile(r"^([A-Z]+)(\d{6})([CP])(\d{8})$")

    today = datetime.now()
    max_expiry = today + timedelta(days=45)

    # First pass: find the single nearest valid expiry date among puts
    expiries = set()
    for symbol in chain.keys():
        match = pattern.match(symbol)
        if not match:
            continue
        _, date_str, opt_type, _ = match.groups()
        if opt_type != "P":
            continue
        try:
            expiry = datetime.strptime(date_str, "%y%m%d")
        except ValueError:
            continue
        if today <= expiry <= max_expiry:
            expiries.add(expiry)

    if not expiries:
        print("No valid expiries found in range.")
        return None

    nearest_expiry = min(expiries)
    nearest_expiry_str = nearest_expiry.strftime("%y%m%d")
    print(f"Using nearest expiry: {nearest_expiry.date()}")

    # Second pass: collect candidates only at that one expiry, tight strike range
    candidates = []
    for symbol in chain.keys():
        match = pattern.match(symbol)
        if not match:
            continue
        _, date_str, opt_type, strike_str = match.groups()
        if opt_type != "P" or date_str != nearest_expiry_str:
            continue
        strike = int(strike_str) / 1000
        if current_price and not (0.90 * current_price <= strike <= 1.02 * current_price):
            continue
        candidates.append(symbol)

    print(f"Filtered down to {len(candidates)} candidate puts at nearest expiry")

    if not candidates:
        return None

    # Batch fetch Greeks for all candidates in ONE call
    request = OptionSnapshotRequest(symbol_or_symbols=candidates)
    snapshots = option_client.get_option_snapshot(request)

    best_symbol = None
    best_diff = None
    for symbol in candidates:
        snapshot = snapshots.get(symbol)
        if snapshot is None or snapshot.greeks is None:
            continue
        delta = snapshot.greeks.delta
        if delta is None:
            continue
        diff = abs(delta - target_mid)
        if best_diff is None or diff < best_diff:
            best_diff = diff
            best_symbol = symbol

    return best_symbol
   