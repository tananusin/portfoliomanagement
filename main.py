# main.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from asset_data import AssetData
from load_assets import load_assets_from_google_sheet
from portfolio_value import enrich_assets, calculate_portfolio_total, assign_weights
from portfolio_view import get_individual_df, get_summarized_df

# Streamlit page config
st.set_page_config(page_title="Portfolio Management", layout="centered")
st.title("📊 Portfolio Management")

# Load Google Sheet and Create AssetData objects
sheet_url = st.secrets["google_sheet"]["url"]
assets = load_assets_from_google_sheet(sheet_url)

# Fetch price, fx, and calculate values
with st.spinner("Fetching live prices and FX rates..."):
    assets = enrich_assets(assets)
    total_thb = calculate_portfolio_total(assets)
    assign_weights(assets, total_thb)

# Create DataFrame
individual_df = get_individual_df(assets)

portfolio_df = individual_df if show_individual else summarized_df

# --- Format and Display Table ---
show_cols = ["name", "weight", "type"]
format_dict = {
    "weight": lambda x: f"{x * 100:.1f}%" if x is not None else "-",
}
st.dataframe(portfolio_df[show_cols].style.format(format_dict))

# --- Pie Chart ---
st.subheader("📈 Allocation Pie Chart")

chart_df = portfolio_df[["name", "value (thb)"]].copy()
chart_df["weight (%)"] = (chart_df["value (thb)"] / total_thb * 100).round(2)

# Filter Out <1% Weight Asset
chart_df = chart_df[chart_df["weight (%)"] >= 1]

# Pie Chart
fig, ax = plt.subplots()
chart_df.set_index("name")["weight (%)"].plot.pie(
    autopct="%1.0f%%",
    figsize=(5, 5),
    ylabel="",
    ax=ax
)
st.pyplot(fig)
