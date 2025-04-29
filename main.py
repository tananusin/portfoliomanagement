# main.py
import streamlit as st
import pandas as pd

from asset_data import AssetData
from load_assets import load_assets_from_google_sheet
from portfolio_value import enrich_assets, calculate_portfolio_total, assign_weights
from user_preferences import get_user_preferences
from portfolio_proportion import assign_targets
from portfolio_view import get_portfolio_df, show_portfolio_table, show_allocation_pie_chart

# Streamlit page config
st.set_page_config(page_title="📊 Portfolio Management", layout="centered")
st.title("Portfolio Management")

# Load Google Sheet and Create AssetData objects
sheet_url = st.secrets["google_sheet"]["url"]
assets = load_assets_from_google_sheet(sheet_url)

# Fetch price, fx, and calculate values
with st.spinner("Fetching live prices and FX rates..."):
    assets = enrich_assets(assets)
    total_thb = calculate_portfolio_total(assets)
    assign_weights(assets, total_thb)

# Sidebar for User Preference 
investment_pct = get_user_preferences()

# Dynamic Target Position Size For Each Asset
assign_targets(assets, investment_pct)

# Create DataFrame
portfolio_df = get_portfolio_df(assets)

# --- Display Table ---
show_portfolio_table(portfolio_df)

# --- Display Pie Chart ---
show_allocation_pie_chart(portfolio_df, total_thb)

