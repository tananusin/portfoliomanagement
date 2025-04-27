import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from load_assets import load_assets_from_google_sheet
from asset_data import AssetData
from portfolio_value import enrich_assets, calculate_portfolio_total, assign_weights

# Streamlit page config
st.set_page_config(page_title="Portfolio Management", layout="centered")
st.title("📊 Portfolio Management")

# Load Google Sheet
sheet_url = st.secrets["google_sheet"]["url"]
assets = load_assets_from_google_sheet(sheet_url)

# Fetch price, fx, and calculate values
with st.spinner("Fetching live prices and FX rates..."):
    assets = enrich_assets(assets)
    total_thb = calculate_portfolio_total(assets)
    assign_weights(assets, total_thb)

# Convert back to DataFrame for display
portfolio_df = pd.DataFrame([{
    "name": asset.name,
    "symbol": asset.symbol,
    "currency": asset.currency,
    "shares": asset.shares,
    "price": asset.price,
    "fx rate": asset.fx_rate,
    "value (thb)": asset.value_thb,
    "weight": asset.weight,
    "target": asset.target,
    "type": asset.asset_type
} for asset in assets])

# Portfolio Table
st.subheader("📄 Portfolio Breakdown")
show_cols = ["name", "symbol", "currency", "shares", "price", "fx rate", "value (thb)", "weight", "target", "type"]
format_dict = {
    "shares": "{:,.2f}",
    "price": "{:,.2f}",
    "fx rate": "{:,.2f}",
    "value (thb)": "{:,.0f}",
    "weight": lambda x: f"{x * 100:.1f}%",
    "target": lambda x: f"{x * 100:.1f}%" if x != 0.0 else "-",
}
st.dataframe(portfolio_df[show_cols].style.format(format_dict))

# Total Portfolio Value
st.metric("💰 Total Portfolio Value (THB)", f"฿{total_thb:,.0f}")

# Pie Chart (All assets individually, no cash grouping)
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
