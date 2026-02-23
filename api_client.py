import yfinance as yf
from decimal import Decimal

def get_realtime_price(symbol: str) -> Decimal | None:
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d", interval="1m")
    if data.empty:
        return None
    last_price = data["Close"].iloc[-1]
    return Decimal(str(last_price))
