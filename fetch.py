# fetch.py
import yfinance as yf

def get_price(symbol):
    try:
        price = yf.Ticker(symbol).history(period="1d")["Close"].iloc[-1]
        return round(price, 2)
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None