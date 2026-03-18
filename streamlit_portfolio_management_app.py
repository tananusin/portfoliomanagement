#streamlit_portfolio_management_app.py
import streamlit as st
import pandas as pd

from asset_data import AssetData
from class_portfolio import RiskClass, RISK_CLASSES
from user_preferences import UserPreference, get_user_preferences

from load_assets import load_assets_from_google_sheet, ensure_reserve_assets_per_currency
from portfolio_value import summarize_assets, combine_assets, calculate_portfolio_total, assign_weights
from assumption import calculate_assumptions
from investment_allocation import apply_asset_class_erc, apply_risk_class_erc, apply_final_asset_targets
from reserve_allocation import build_currency_portfolio, assign_reserve_asset_targets

from position_size import assign_position_sizes
from price_signal import assign_price_signals
from pe_signal import assign_pe_signals
from yield_signal import assign_yield_signals

from portfolio_view import (
    get_portfolio_df,
    show_summary_signal_table, show_position_table, show_price_signal_table, show_pe_signal_table, show_yield_signal_table,
    show_google_sheet_data_table,
    show_allocation_pie_chart, show_target_allocation_pie_chart,
)
from risk_contribution_view import show_risk_asset_table, show_risk_class_table, show_currency_table

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
    
assets = ensure_reserve_assets_per_currency(assets)

# --- Portfolio Calculations ---
assets = summarize_assets(assets)
total_thb = calculate_portfolio_total(assets)
current_portfolio_mdd= assign_weights(assets, total_thb)
calculate_assumptions(assets, user_pref)

# # --- Assign Target Weight to Investment Portfolio                                                                        
core_mdd = apply_asset_class_erc(assets, RISK_CLASSES, "Core")                    # Asset ERC inside each class
growth_mdd = apply_asset_class_erc(assets, RISK_CLASSES, "Growth")
speculative_mdd = apply_asset_class_erc(assets, RISK_CLASSES, "Speculative") 

investment_portfolio_mdd = apply_risk_class_erc(RISK_CLASSES)                     # Class ERC using dynamic class_mdd
target_portfolio_mdd = user_pref.investment_weight * investment_portfolio_mdd
apply_final_asset_targets(assets, RISK_CLASSES, user_pref.investment_weight)      # Final asset portfolio targets


# # --- Assign Target Weight to Reserve Portfolio
cash_weight = user_pref.investment_weight * investment_portfolio_mdd
reserve_weight = 1 - user_pref.investment_weight
gold_weight = reserve_weight * user_pref.gold_weight_reserve
bond_weight_total = reserve_weight - cash_weight - gold_weight

# If reserve is not enough, reduce gold first
if bond_weight_total < 0:
    gold_weight = gold_weight + bond_weight_total
    bond_weight_total = 0.0

# If gold also becomes negative, reserve is insufficient
if gold_weight < 0:
    st.error("❌ Not sufficient cash. Please decrease investment weight.")
    st.stop()
    
apply_final_asset_targets(assets, RISK_CLASSES, user_pref.investment_weight)

currencies, currency_map = build_currency_portfolio(assets=assets, bond_weight_total=bond_weight_total,)
assign_reserve_asset_targets(assets, currencies, gold_weight)


# # --- Assign Signals
assign_position_sizes(assets, user_pref)
assign_price_signals(assets, user_pref.years_rebound)
assign_pe_signals(assets)
assign_yield_signals(assets)


# --- Convert to DataFrame ---
portfolio_df = get_portfolio_df(assets)

# --- Display Tables ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["🚦 Signals", "🎯 Position", "💹 Price Signal",  "📜 PE Signal", "💵 Yield Signal", "📄 Google Sheet", "📉 Risk"])
with tab1:
    st.subheader("🚦 Portfolio Signals")
    show_summary_signal_table(portfolio_df)
with tab2:
    st.subheader("🎯 Position")
    show_position_table(portfolio_df)
with tab3:
    st.subheader("💹 Price Signal")
    show_price_signal_table(portfolio_df)
    st.caption(f"""
    ℹ️ Calmar ratio = annualized return over the past {user_pref.years_rebound} years divided by the assumed MDD.  
    ℹ️ Don't use Calmar ratio when the asset's price crashes.
    """)
with tab4:
    st.subheader("📜 PE Signal")
    show_pe_signal_table(portfolio_df)
with tab5:
    st.subheader("💵 Yield Signal")
    show_yield_signal_table(portfolio_df)
with tab6:
    st.subheader("📄 Google Sheet Format")
    show_google_sheet_data_table(portfolio_df)
    st.caption(f"""
    ℹ️ "Years low" shows the lowest market price in the last {user_pref.years_rebound} years.  
    ℹ️ "PE p25" shows the PE ratio 25th percentile in the last {user_pref.years_rebound} years.  
    ℹ️ "PE p75" shows the PE ratio 75th percentile in the last {user_pref.years_rebound} years.
    """)
with tab7:
    st.subheader("📉 Risk Contribution")
    show_risk_asset_table(portfolio_df)
    show_risk_class_table(RISK_CLASSES)
    show_currency_table(currencies)




# --- Display Pie Charts ---
assets_combine = combine_assets(assets)
portfolio_combine_df = get_portfolio_df(assets_combine)

tab1, tab2 = st.tabs(["📊 Actual", "🎯 Target"])
with tab1:
    st.subheader("📊 Actual Allocation Pie Chart")
    show_allocation_pie_chart(portfolio_combine_df, total_thb)
    st.write(f"Estimated Current Portfolio MDD: **{current_portfolio_mdd:.0%}**")
with tab2:
    st.subheader("🎯 Target Allocation Pie Chart")
    show_target_allocation_pie_chart(portfolio_combine_df)
    st.write(f"Estimated Target Portfolio MDD: **{target_portfolio_mdd:.0%}**")


