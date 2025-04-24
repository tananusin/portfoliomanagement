#valuation.py
import streamlit as st
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
        hist_price = ticker.history(period="3y")
        eps_ttm = ticker.info.get("trailingEps")

        if eps_ttm is None or eps_ttm <= 0:
            return None

        hist_price["PE"] = hist_price["Close"] / eps_ttm
        pe_series = hist_price["PE"].dropna()

        if pe_series.empty:
            return None

        current_pe = pe_series.iloc[-1]
        percentile = (pe_series < current_pe).mean() * 100
        st.write(f"PE percentile for {ticker_symbol} is: {percentile:.2f}%")
        return percentile

    except Exception as e:
        return None
