# main.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from asset_data import AssetData
from load_assets import load_assets_from_google_sheet
from portfolio_value import enrich_assets, calculate_portfolio_total, assign_weights

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

# --- Create two versions of DataFrame ---

# (1) Individual asset view
individual_df = pd.DataFrame([{
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

# (2) Summarized view (Bond + Cash total)
def create_summarized_df(assets, total_thb):
    bond_total_value = 0
    cash_total_value = 0
    bond_total_target = 0
    cash_total_target = 0
    other_assets = []

    for asset in assets:
        if asset.asset_type.lower() == "bond":
            bond_total_value += asset.value_thb or 0
            bond_total_target += asset.target or 0
        elif asset.asset_type.lower() == "cash":
            cash_total_value += asset.value_thb or 0
            cash_total_target += asset.target or 0
        else:
            other_assets.append(asset)

    summarized = [{
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
    } for asset in other_assets]

    # Add Total Bond and Cash at the end
    if bond_total_value > 0:
        summarized.append({
            "name": "Total Bonds",
            "symbol": "BOND",
            "currency": "THB",
            "shares": "-",
            "price": "-",
            "fx rate": "-",
            "value (thb)": bond_total_value,
            "weight": bond_total_value / total_thb,
            "target": bond_total_target,
            "type": "Bond"
        })
    if cash_total_value > 0:
        summarized.append({
            "name": "Total Cash",
            "symbol": "CASH",
            "currency": "THB",
            "shares": "-",
            "price": "-",
            "fx rate": "-",
            "value (thb)": cash_total_value,
            "weight": cash_total_value / total_thb,
            "target": cash_total_target,
            "type": "Cash"
        })

    return pd.DataFrame(summarized)

summarized_df = create_summarized_df(assets, total_thb)

# --- UI Toggle ---
st.subheader("📄 Portfolio Breakdown")
view_option = st.radio(
    "View Mode:",
    ("Summarized (Bond+Cash Grouped)", "Individual Assets"),
    index=0
)

if view_option == "Summarized (Bond+Cash Grouped)":
    portfolio_df = summarized_df
else:
    portfolio_df = individual_df

# --- Format and Display Table ---
show_cols = ["name", "symbol", "currency", "shares", "price", "fx rate", "value (thb)", "weight", "target", "type"]
format_dict = {
    "shares": "{:,.2f}" if portfolio_df["shares"].dtype != object else None,
    "price": "{:,.2f}" if portfolio_df["price"].dtype != object else None,
    "fx rate": "{:,.2f}" if portfolio_df["fx rate"].dtype != object else None,
    "value (thb)": "{:,.0f}",
    "weight": lambda x: f"{x * 100:.1f}%" if isinstance(x, (int, float)) else "-",
    "target": lambda x: f"{x * 100:.1f}%" if isinstance(x, (int, float)) else "-"
}

st.dataframe(portfolio_df[show_cols].style.format(format_dict))

# --- Total Portfolio Value ---
st.metric("💰 Total Portfolio Value (THB)", f"฿{total_thb:,.0f}")

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
