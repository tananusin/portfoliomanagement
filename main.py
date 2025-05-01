# main.py
import streamlit as st
import pandas as pd

from asset_data import AssetData
from load_assets import load_assets_from_google_sheet
from portfolio_value import enrich_assets, summarize_assets, calculate_portfolio_total, assign_weights
from user_preferences import get_user_preferences, UserPreference
from portfolio_proportion import assign_targets
from portfolio_size import set_all_position_sizes
from portfolio_view import get_portfolio_df, show_portfolio_table, show_allocation_pie_chart

# Streamlit page config
st.set_page_config(page_title="Portfolio Management", layout="centered")
st.title("📊 Portfolio Management")

# Load Google Sheet and Create AssetData objects
sheet_url = st.secrets["google_sheet"]["url"]
assets = load_assets_from_google_sheet(sheet_url)

# Sidebar for User Preference 
user_pref = get_user_preferences()

# Validate the password
if user_pref.password == st.secrets["credentials"]["app_password"]:
    st.success("Password Correct! Fetching live data...")
    
    # Fetch price, fx, and 
    with st.spinner("Fetching live prices and FX rates..."):
        assets = enrich_assets(assets)
else:
    st.warning("Offline Mode: Using Portfolio Data From Google Sheet.")
    
# Calculate Portfolio Values
assets = summarize_assets(assets)
total_thb = calculate_portfolio_total(assets)
assign_weights(assets, total_thb)

# Calulate Position Size for All Assets()
set_all_position_sizes(assets)

# Dynamic Target Position Size For Each Asset
assign_targets(assets, user_pref.investment_pct)

# Create DataFrame
portfolio_df = get_portfolio_df(assets)

# --- Display Table ---
show_portfolio_table(portfolio_df)

# --- Display Pie Chart ---
show_allocation_pie_chart(portfolio_df, total_thb)

