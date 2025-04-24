import yfinance as yf
import numpy as np
import pandas as pd

def valuation(ticker_symbol)

try:
  ticker = yf.Ticker(ticker_symbol)
