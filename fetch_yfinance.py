# fetch_yfinance.py
import yfinance as yf

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
        return round(pe_ratio, 2) if pe_ratio else None
    except Exception:
        return None

def get_trailing_dividend_yield(symbol: str) -> float | None:
    try:
        ticker = yf.Ticker(symbol.strip().upper())
        dividend_rate = ticker.info.get("dividendRate")
        current_price = ticker.info.get("regularMarketPrice")

        if dividend_rate and current_price:
            # Calculate trailing dividend yield as a percentage
            dividend_yield = (dividend_rate / current_price) * 100
            return round(dividend_yield, 2)
        return None
    except Exception:
        return None


