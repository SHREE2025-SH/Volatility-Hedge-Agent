from app.execution import place_put_order

# Use the put symbol we found earlier as a test
order = place_put_order("SPY260902P00765000", quantity=1)
print("Order ID:", order.id)
print("Status:", order.status)
print("Symbol:", order.symbol)