#streamlit_portfolio_management_app.py
import streamlit as st
import pandas as pd

from asset_data import AssetData
from config import RiskClass, RISK_CLASSES, THRESHOLD_DRIFT, THRESHOLD_DRIFT_RELATIVE
from user_preferences import UserPreference, get_user_preferences

from load_assets import load_assets_from_google_sheet
from portfolio_value import summarize_assets, combine_assets, calculate_portfolio_total, assign_weights
from assumption import calculate_assumptions
from erc import (
    apply_asset_class_erc,
    apply_risk_class_erc,
    apply_final_asset_targets,
)
from portfolio_proportion import assign_targets
from position_size import assign_position_sizes
from price_change import assign_price_changes
from yield_signal import assign_yield_signals
from portfolio_view import get_portfolio_df, show_debug_table, show_portfolio_table, show_google_sheet_data_table, show_summary_signal_table, show_price_change_table, show_pe_signal_table, show_yield_signal_table, show_allocation_pie_chart, show_target_allocation_pie_chart
from pe_percentile import display_pe_percentiles


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


# --- Portfolio Calculations ---
assets = summarize_assets(assets)
total_thb = calculate_portfolio_total(assets)
assign_weights(assets, total_thb)
calculate_assumptions(assets, user_pref)

# # --- Assign Target Weight to Investment Portfolio
# 1) calculate asset weights inside each class
apply_asset_class_erc(assets, "Core")
apply_asset_class_erc(assets, "Growth")
apply_asset_class_erc(assets, "Speculative")

# 2) calculate class weights in investment portfolio
portfolio_mdd = apply_risk_class_erc(RISK_CLASSES)

# 3) calculate final asset target weights
apply_final_asset_targets(assets, RISK_CLASSES)

# # --- Assign Dynamic Target and Position ---
# assign_targets(assets, user_pref)
# assign_position_sizes(assets)
# assign_price_changes(assets, user_pref)

# # --- Assign PE Signal ---
# assign_pe_signals(assets)

# # --- Assign Yield Signal ---
# assign_yield_signals(assets, user_pref)


# --- Convert to DataFrame ---
portfolio_df = get_portfolio_df(assets)

# --- Display Tables ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📋 Portfolio", "🚦 Signals", "📉 Price Signal",  "💹 PE Signal", "💵 Yield Signal", "📄 Google Sheet Data", "🐞 Debug"])
with tab1:
    st.subheader("📋 Portfolio Report")
    show_portfolio_table(portfolio_df)
    st.metric("💰 Total Portfolio Value (THB)", f"฿{total_thb:,.0f}")
with tab2:
    st.subheader("🚦 Portfolio Signals")
    # show_summary_signal_table(portfolio_df)
with tab3:
    st.subheader("📉 Price Signal")
    # show_price_change_table(portfolio_df)
with tab4:
    st.subheader("💹 PE Signal")
    # show_pe_signal_table(portfolio_df)
with tab5:
    st.subheader("💵 Yield Signal")
    # show_yield_signal_table(portfolio_df)
with tab6:
    st.subheader("📄 Google Sheet Data")
    show_google_sheet_data_table(portfolio_df)
    st.caption(f"""
    ℹ️ "Years low" shows the lowest market price in the last {user_pref.years_rebound} years.  
    ℹ️ "PE p25" shows the PE ratio 25th percentile in the last {user_pref.years_rebound} years.  
    ℹ️ "PE p75" shows the PE ratio 75th percentile in the last {user_pref.years_rebound} years.
    """)
with tab7:
    st.subheader("💵 Debug Table")
    show_debug_table(portfolio_df)



# --- Display Pie Charts ---
assets_combine = combine_assets(assets)
portfolio_combine_df = get_portfolio_df(assets_combine)

tab1, tab2 = st.tabs(["📊 Actual", "🎯 Target"])
with tab1:
    st.subheader("📊 Actual Allocation Pie Chart")
    show_allocation_pie_chart(portfolio_combine_df, total_thb)
with tab2:
    st.subheader("🎯 Target Allocation Pie Chart")
    # show_target_allocation_pie_chart(portfolio_df)


