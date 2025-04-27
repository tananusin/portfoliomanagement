# fetch.py
import yfinance as yf

def get_price(symbol: str) -> float:
    """Fetches the market price for the asset symbol."""
    symbol_clean = str(symbol).strip().upper()
    try:
        ticker = yf.Ticker(symbol_clean)
        return ticker.info.get("regularMarketPrice", None)  # Safe access to avoid key errors
    except Exception as e:
        return None  # Return None if there's an error

def get_fx_to_thb(currency: str) -> float:
    """Fetches the exchange rate from the given currency to THB."""
    try:
        pair = f"{currency}THB=X"
        fx = yf.Ticker(pair).history(period="1d")
        return round(fx["Close"].iloc[-1], 2)  # Fetch the latest FX rate and round it
    except Exception as e:
        return None  # Return None if there's an error