# fetch_yfinance.py
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def can_fetch_data(test_symbol: str = "AAPL") -> bool:
    """Test if live data can be fetched successfully (e.g., not rate-limited or offline)."""
    try:
        ticker = yf.Ticker(test_symbol)
        price = ticker.info.get("regularMarketPrice", None)
        return price is not None
    except Exception:
        return False

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

def get_52_week_high(symbol: str) -> float | None:
    try:
        ticker = yf.Ticker(symbol.strip().upper())
        return ticker.fast_info.get("yearHigh")
    except Exception:
        return None

def get_52_week_low(symbol: str) -> float | None:
    try:
        ticker = yf.Ticker(symbol.strip().upper())
        return ticker.fast_info.get("yearLow")
    except Exception:
        return None

def get_trailing_pe(symbol: str) -> float | None:
    """Fetches the trailing P/E ratio for the asset symbol."""
    try:
        ticker = yf.Ticker(symbol.strip().upper())
        pe_ratio = ticker.info.get("trailingPE")
        
        # Set P/E to 0.0 if None or not available
        if pe_ratio is None:
            return 0.0
        
        return round(pe_ratio, 2) if pe_ratio else None
    except Exception:
        return None

def get_trailing_dividend_yield(symbol: str) -> float | None:
    try:
        ticker = yf.Ticker(symbol.strip().upper())
        dividend_rate = ticker.info.get("dividendRate")
        current_price = ticker.info.get("regularMarketPrice")

        # Check if dividend rate or current price is None or zero
        if dividend_rate is None or current_price is None or current_price == 0:
            return 0.0

        # Calculate trailing dividend yield as a percentage
        dividend_yield = dividend_rate / current_price
        return round(dividend_yield, 4)
    except Exception:
        return None

def get_pe_percentiles(symbol: str, months: int):
    try:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=months * 30)

        ticker = yf.Ticker(symbol)
        hist = ticker.history(start=start_date.strftime('%Y-%m-%d'),
                              end=end_date.strftime('%Y-%m-%d'),
                              interval='1mo')

        info = ticker.info
        trailing_eps = info.get('trailingEps')

        if hist.empty:
            return None, None
        if trailing_eps in [None, 0]:
            return None, None

        hist = hist[hist['Close'] > 0]
        hist['PE'] = hist['Close'] / trailing_eps
        hist = hist[hist['PE'] < 1000]  # filter extreme outliers

        pe_series = hist['PE']
        percentiles = np.percentile(pe_series, [25, 75])
        return float(percentiles[0]), float(percentiles[1])

    except Exception:
        return None, None
