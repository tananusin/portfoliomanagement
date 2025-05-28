# streamlit_portfolio_report_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List

from asset_data import AssetData
from load_assets import load_assets_from_google_sheet
from fetch_yfinance import can_fetch_data
from portfolio_value import enrich_assets, calculate_asset_values, calculate_portfolio_total, assign_weights

# --- User Preference Dataclass ---
@dataclass
class UserPreference:
    password: str
    sheet_url: str

# --- Helper Functions ---
def convert_to_csv_url(sheet_url: str) -> str:
    sheet_url = sheet_url.strip()
    if "/edit" in sheet_url:
        return sheet_url.split("/edit")[0] + "/export?format=csv"
    elif sheet_url.endswith("/export?format=csv"):
        return sheet_url
    else:
        raise ValueError("Invalid Google Sheet link format.")

def get_user_preferences() -> UserPreference:
    st.sidebar.header("🛠️ User Preference")

    st.sidebar.markdown("### 📄 Google Sheet Source")
    input_url = st.sidebar.text_input(
        label="Enter your Google Sheet URL (optional)",
        placeholder="https://docs.google.com/spreadsheets/d/...",
        help="Leave blank to use the default shared sheet."
    )
    st.sidebar.caption("ℹ️ Paste a shared Google Sheet link ending in `/edit?usp=sharing`.")

    try:
        sheet_url = convert_to_csv_url(input_url) if input_url else st.secrets["google_sheet"]["url"]
    except ValueError:
        st.sidebar.error("❌ Invalid link format.")
        sheet_url = st.secrets["google_sheet"]["url"]

    st.sidebar.markdown("### 🔑 Switch to Live Data")
    password = st.sidebar.text_input(
        "Enter password for live data access:",
        type="password"
    )

    return UserPreference(password=password, sheet_url=sheet_url)

def get_portfolio_df(assets: List[AssetData]) -> pd.DataFrame:
    return pd.DataFrame([{
        "name": asset.name,
        "currency": asset.currency,
        "shares": asset.shares,
        "price": asset.price,
        "fx rate": asset.fx_rate,
        "value (thb)": asset.value_thb,
        "weight": asset.weight,
        "52w high": asset.peak_1y,
        "52w low": asset.trough_1y,
        "pe": asset.pe_ratio,
        "yield": asset.dividend_yield,
    } for asset in assets])

def show_portfolio_table(portfolio_df: pd.DataFrame):
    st.subheader("📋 Portfolio Report")
    show_cols = ["name", "currency", "shares", "price", "fx rate", "value (thb)", "weight"]
    format_dict = {
        "shares": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "price": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "fx rate": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "value (thb)": lambda x: f"{x:,.0f}" if x != 0.0 else "-",
        "weight": lambda x: f"{x * 100:.1f}%" if x is not None else "-",
    }
    st.dataframe(portfolio_df[show_cols].style.format(format_dict))

def show_market_data_table(portfolio_df: pd.DataFrame):
    st.subheader("📋 Market Data")
    show_cols = ["name", "currency", "price", "fx rate", "52w high", "52w low", "pe", "yield"]
    format_dict = {
        "price": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "fx rate": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "52w high": lambda x: f"{x:,.2f}" if x else "-",
        "52w low": lambda x: f"{x:,.2f}" if x else "-",
        "pe": lambda x: f"{x:,.0f}" if pd.notnull(x) and x != 0.0 else "-",
        "yield": lambda x: f"{x * 100:.1f}%" if x not in [None, 0.0] else "-",
    }
    st.dataframe(portfolio_df[show_cols].style.format(format_dict))

def show_allocation_pie_chart(portfolio_df: pd.DataFrame, total_thb: float):
    st.subheader("📊 Actual Allocation Pie Chart")
    chart_df = portfolio_df[["name", "value (thb)"]].copy()
    chart_df["weight (%)"] = (chart_df["value (thb)"] / total_thb * 100).round(2)
    chart_df = chart_df[chart_df["weight (%)"] >= 1]

    fig, ax = plt.subplots()
    chart_df.set_index("name")["weight (%)"].plot.pie(
        autopct="%1.0f%%", figsize=(5, 5), ylabel="", ax=ax
    )
    st.pyplot(fig)







# --- Streamlit Page Config ---
st.set_page_config(page_title="Portfolio Report", layout="centered")
st.title("🗂️ Portfolio Report")

# --- Load User Preferences ---
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

# --- Calculate Values (Without Summarization) ---
for asset in assets:
    calculate_asset_values(asset)
total_thb = calculate_portfolio_total(assets)
assign_weights(assets, total_thb)

# --- Display Table ---
portfolio_df = get_portfolio_df(assets)
tab1, tab2 = st.tabs(["📋 Portfolio", "🧾 Market Data"])
with tab1:
    show_portfolio_table(portfolio_df)
with tab2:
    show_market_data_table(portfolio_df)

# --- Display Metrics ---
st.metric("💰 Total Portfolio Value (THB)", f"฿{total_thb:,.0f}")

# --- Display Chart ---
show_allocation_pie_chart(portfolio_df, total_thb)

