#streamlit_portfolio_report_app.py
import streamlit as st
import pandas as pd

from asset_data import AssetData
from load_assets import load_assets_from_google_sheet
from fetch_yfinance import can_fetch_data
from portfolio_value import enrich_assets, summarize_assets, calculate_portfolio_total, assign_weights

# --- Streamlit Page Config ---
st.set_page_config(page_title="Portfolio Report", layout="centered")
st.title("🗂️ Portfolio Report")

# --- User Preferences ---
user_pref = get_user_preferences()

# --- Load Asset Data ---
try:
    assets = load_assets_from_google_sheet(user_pref.sheet_url)
except Exception:
    st.error("❌ Failed to load data from the provided Google Sheet. Using default sheet instead.")
    assets = load_assets_from_google_sheet(st.secrets["google_sheet"]["url"])

# --- Check Password and Fetch Data ---
if user_pref.password == st.secrets["credentials"]["app_password"]:
    st.success("🔓 Password Correct! Checking live data availability...")
    if can_fetch_data():  # ✅ Check fetch readiness
        with st.spinner("Fetching live prices and FX rates..."):
            assets = enrich_assets(assets)
    else:
        st.error("❌ Unable to fetch live data. Falling back to static data.")
else:
    st.warning("🔒 Offline Mode: Using static data from Google Sheet.")

# --- Portfolio Calculations ---
assets = summarize_assets(assets)
total_thb = calculate_portfolio_total(assets)
assign_weights(assets, total_thb)
