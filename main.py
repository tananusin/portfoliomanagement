import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fetch import get_price, get_fx_to_thb

st.set_page_config(page_title="Portfolio Rebalancer", layout="centered")
st.title("📊 Portfolio Rebalancer")

sheet_url = "https://docs.google.com/spreadsheets/d/1T8H0By9mCahSaG09NOvc4bXGE_cDtDdCMsFoIabDCnw/export?format=csv"

# Load and sanitize columns
try:
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip().str.lower()  # 🔥 Fix column name issues
except Exception as e:
    st.error(f"❌ Failed to load Google Sheet: {e}")
    st.stop()

# Validate required columns
required_cols = {"symbol", "shares", "currency"}
if not required_cols.issubset(df.columns):
    st.error(f"Missing columns in Google Sheet. Required: {required_cols}")
    st.write("Loaded columns:", df.columns.tolist())
    st.stop()

# Fetch data
with st.spinner("Fetching live prices and FX rates..."):
    df["price"] = df["symbol"].apply(get_price)
    df["fx rate"] = df["currency"].apply(get_fx_to_thb)
    df["value (local)"] = df["shares"] * df["price"]
    df["value (thb)"] = df["value (local)"] * df["fx rate"]
    total_thb = df["value (thb)"].sum()
    df["weight (%)"] = (df["value (thb)"] / total_thb * 100).round(2)

# Show breakdown
st.subheader("📄 Portfolio Breakdown")
st.dataframe(df)

# Total metric
st.metric("💰 Total Portfolio Value (THB)", f"฿{total_thb:,.2f}")

# Pie Chart
st.subheader("📈 Allocation Pie Chart")
fig, ax = plt.subplots()
df.set_index("symbol")["weight (%)"].plot.pie(autopct="%1.1f%%", figsize=(5, 5), ylabel="", ax=ax)
st.pyplot(fig)
