# fetch.py
import yfinance as yf

def get_price(symbol):
    symbol_clean = str(symbol).strip().upper()
    if symbol_clean.startswith(("CASH", "BOND")):
        return 1.0
    try:
        ticker = yf.Ticker(symbol_clean)
        return ticker.info["regularMarketPrice"]
    except:
        return None

def get_fx_to_thb(currency):
    if currency == "THB":
        return 1.0
    try:
        pair = f"{currency}THB=X"
        fx = yf.Ticker(pair).history(period="1d")
        return round(fx["Close"].iloc[-1], 2)
    except:
        return None
