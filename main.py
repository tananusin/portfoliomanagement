#main.py
import streamlit as st
import pandas as pd

from asset_data import AssetData
from load_assets import load_assets_from_google_sheet
from portfolio_value import enrich_assets, summarize_assets, calculate_portfolio_total, assign_weights
from user_preferences import get_user_preferences, UserPreference
from portfolio_proportion import assign_targets
from position_size import assign_position_sizes
from price_signal import assign_price_signals
from portfolio_view import get_portfolio_df, show_portfolio_table, show_allocation_pie_chart, show_target_allocation_pie_chart

# Streamlit page config
st.set_page_config(page_title="Portfolio Management", layout="centered")
st.title("🗂️ Portfolio Management")

# Get user preferences (including optional Google Sheet URL and password)
user_pref = get_user_preferences()

# Try to load from user input sheet URL; fallback to default if invalid
try:
    assets = load_assets_from_google_sheet(user_pref.sheet_url)
except Exception as e:
    st.error("❌ Failed to load data from the provided Google Sheet. Using default sheet instead.")
    assets = load_assets_from_google_sheet(st.secrets["google_sheet"]["url"])

# Validate the password for live data
if user_pref.password == st.secrets["credentials"]["app_password"]:
    st.success("🔓 Password Correct! Fetching live data...")
    with st.spinner("Fetching live prices and FX rates..."):
        assets = enrich_assets(assets)
else:
    st.warning("🔒 Offline Mode: Using static data from Google Sheet.")

# Calculate Portfolio Values
assets = summarize_assets(assets)
total_thb = calculate_portfolio_total(assets)
assign_weights(assets, total_thb)

# Dynamic Target Position Size For Each Asset
assign_targets(assets, user_pref)

# Calculate Position Size for All Assets
assign_position_sizes(assets)

# Assign price signal classification
assign_price_signals(assets, user_pref)

# Create DataFrame
portfolio_df = get_portfolio_df(assets)

# --- Display Table ---
show_portfolio_table(portfolio_df)

# --- Display Pie Charts ---
show_allocation_pie_chart(portfolio_df, total_thb)
show_target_allocation_pie_chart(portfolio_df)
