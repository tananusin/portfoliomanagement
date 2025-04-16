# fetch.py
import yfinance as yf

def get_price(symbol):
    if "CASH" in symbol:
        return 1.0    
    try:
        price = yf.Ticker(symbol).history(period="1d")["Close"].iloc[-1]
        return round(price, 2)
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
