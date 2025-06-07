#streamlit_portfolio_management_app.py
import streamlit as st
import pandas as pd

from asset_data import AssetData
from load_assets import load_assets_from_google_sheet
from fetch_yfinance import can_fetch_data
from portfolio_value import enrich_assets, summarize_assets, calculate_portfolio_total, assign_weights
from user_preferences import get_user_preferences, UserPreference
from portfolio_proportion import assign_targets
from position_size import assign_position_sizes
from price_change import assign_price_changes
from pe_signal import assign_pe_signals
from yield_signal import assign_yield_signals
from portfolio_view import get_portfolio_df, show_portfolio_table, show_market_data_table, show_summary_signal_table, show_price_change_table, show_pe_signal_table, show_yield_signal_table, show_allocation_pie_chart, show_target_allocation_pie_chart



# --- Streamlit Page Config ---
st.set_page_config(page_title="Portfolio Management", layout="centered")
st.title("🗂️ Portfolio Management")

# --- User Preferences ---
user_pref = get_user_preferences()

# --- Load Asset Data ---
try:
    assets = load_assets_from_google_sheet(user_pref.sheet_url)
except Exception:
    st.error("❌ Failed to load data from the provided Google Sheet. Using default sheet instead.")
    assets = load_assets_from_google_sheet(st.secrets["google_sheet"]["url"])

# --- Check Password and Fetch Live Data ---
if user_pref.password == st.secrets["credentials"]["app_password"]:
    st.success("🔓 Password Correct! Checking live data availability...")
    if can_fetch_data():
        with st.spinner("Fetching live prices and FX rates..."):
            assets = enrich_assets(assets)
    else:
        st.error("❌ Unable to fetch live data. Falling back to static data.")
else:
    st.warning("🔒 Offline Mode: Using static data from Google Sheet.")

# --- For Showing Unsummarized Market Data ---
portfolio_unsum_df = get_portfolio_df(assets)

# --- Portfolio Calculations ---
assets = summarize_assets(assets)
total_thb = calculate_portfolio_total(assets)
assign_weights(assets, total_thb)

# --- Assign Dynamic Target and Position ---
assign_targets(assets, user_pref)
assign_position_sizes(assets)
assign_price_changes(assets, user_pref)

# --- Assign PE Signal ---
assign_pe_signals(assets)

# --- Assign Yield Signal ---
assign_yield_signals(assets, user_pref)

# --- Convert to DataFrame ---
portfolio_df = get_portfolio_df(assets)

# --- Display Tables ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📋 Portfolio", "📈 Signals", "🧮 Price Change",  "🧮 PE Signal", "🧮 Yield Signal", "💹 Market Data"])
with tab1:
    show_portfolio_table(portfolio_df)
    st.metric("💰 Total Portfolio Value (THB)", f"฿{total_thb:,.0f}")
with tab2:
    show_summary_signal_table(portfolio_df)
with tab3:
    show_price_change_table(portfolio_df)
with tab4:
    show_pe_signal_table(portfolio_df)
with tab5:
    show_yield_signal_table(portfolio_df)
with tab6:
    show_market_data_table(portfolio_unsum_df)


# --- Display Pie Charts ---
tab1, tab2 = st.tabs(["📋 Actual", "🎯 Target"])
with tab1:
    show_allocation_pie_chart(portfolio_df, total_thb)
with tab2:
    show_target_allocation_pie_chart(portfolio_df)


