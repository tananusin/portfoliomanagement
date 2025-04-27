import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from asset_data import AssetData
from portfolio_value import enrich_assets, calculate_portfolio_total, assign_weights

# Streamlit page config
st.set_page_config(page_title="Portfolio Report", layout="centered")
st.title("📊 Portfolio Report")

# Load Google Sheet
sheet_url = st.secrets["google_sheet"]["url"]
sheet_url = sheet_url.replace('/edit#gid=', '/gviz/tq?tqx=out:csv&gid=')

# Load and clean data
try:
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip().str.lower()
except Exception as e:
    st.error(f"❌ Failed to load Google Sheet: {e}")
    st.stop()

# Validate columns
required_cols = {"name", "symbol", "type", "currency", "shares", "target"}
if not required_cols.issubset(df.columns):
    st.error(f"Missing columns in Google Sheet. Required: {required_cols}")
    st.write("Loaded columns:", df.columns.tolist())
    st.stop()

# Create AssetData objects
assets = [
    AssetData(
        name=row["name"],
        symbol=row["symbol"],
        asset_type=row["type"],
        currency=row["currency"],
        shares=row["shares"],
        target=row["target"]
    )
    for _, row in df.iterrows()
]

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
    "currency": asset.asset_type,
    "shares": asset.shares,
    "price": asset.price,
    "fx rate": asset.fx_rate,
    "value (thb)": asset.value_thb,
    "weight": asset.weight,
    "target": asset.target
} for asset in assets])

# Portfolio Table
st.subheader("📄 Portfolio Breakdown")
show_cols = ["name", "symbol", "currency", "type", "shares", "price", "fx rate", "value (thb)", "weight", "target"]
format_dict = {
    "shares": "{:,.2f}",
    "price": "{:,.2f}",
    "fx rate": "{:,.2f}",
    "value (thb)": "{:,.0f}",
    "weight": lambda x: f"{x * 100:.1f}%",
    "target": lambda x: f"{x * 100:.1f}%",
}
st.dataframe(portfolio_df[show_cols].style.format(format_dict))

# Total Portfolio Value
st.metric("💰 Total Portfolio Value (THB)", f"฿{total_thb:,.0f}")

# Prepare Pie Chart (Cash summarized)
cash_mask = portfolio_df["name"].str.upper().str.startswith("CASH")
cash_df = portfolio_df[cash_mask]
non_cash_df = portfolio_df[~cash_mask]

if not cash_df.empty:
    cash_value = cash_df["value (thb)"].sum()
    cash_row = pd.DataFrame([{
        "name": "Cash",
        "value (thb)": cash_value
    }])
    chart_df = pd.concat([non_cash_df[["name", "value (thb)"]], cash_row], ignore_index=True)
else:
    chart_df = non_cash_df[["name", "value (thb)"]]

chart_df["weight (%)"] = (chart_df["value (thb)"] / total_thb * 100).round(2)
chart_df_filtered = chart_df[chart_df["weight (%)"] >= 1]

# Pie Chart
st.subheader("📈 Allocation Pie Chart")
fig, ax = plt.subplots()
chart_df_filtered.set_index("name")["weight (%)"].plot.pie(
    autopct="%1.0f%%", figsize=(5, 5), ylabel="", ax=ax
)
st.pyplot(fig)
