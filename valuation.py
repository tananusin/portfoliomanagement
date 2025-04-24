#valuation.py
import yfinance as yf
import numpy as np
import pandas as pd

pe_percentile_value = None  # Global variable to store the percentile result

def pe_percentile(ticker_symbol: str):
    """
    Calculate the percentile rank of the current P/E compared to the past 3 years.
    Saves the percentile into pe_percentile_value for further calculations.
    """
    global pe_percentile_value

    try:
        ticker = yf.Ticker(ticker_symbol)

        # Get historical data and current trailing EPS
        hist_price = ticker.history(period="3y")
        eps_ttm = ticker.info.get("trailingEps")

        if eps_ttm is None or eps_ttm <= 0:
            print("EPS is not available or invalid")
            pe_percentile_value = None
            return

        # Calculate historical P/E series
        hist_price["PE"] = hist_price["Close"] / eps_ttm
        pe_series = hist_price["PE"].dropna()

        if pe_series.empty:
            print("PE series is empty")
            pe_percentile_value = None
            return

        # Get current P/E and compute percentile rank
        current_pe = pe_series.iloc[-1]
        pe_percentile_value = (pe_series < current_pe).mean() * 100

        print(f"PE percentile for {ticker_symbol} is: {pe_percentile_value:.2f}%")

    except Exception as e:
        print(f"Error processing {ticker_symbol}: {e}")
        pe_percentile_value = None
