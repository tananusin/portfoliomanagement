import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fetch import get_price, get_fx_to_thb

st.set_page_config(page_title="Portfolio Rebalancer", layout="centered")

st.title("📊 Portfolio Rebalancer")
st.markdown("Track your holdings in **real-time** and convert to THB 🇹🇭")

# Replace this with your actual CSV export link from Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/1T8H0By9mCahSaG09NOvc4bXGE_cDtDdCMsFoIabDCnw/export?format=csv"

# Load data
try:
    df = pd.read_csv(sheet_url)
    st.write(df.columns)  # Check column names
except Exception as e:
    st.error(f"❌ Failed to load Google Sheet. Error: {e}")
    st.stop()

# Fetch prices and FX rates
with st.spinner("Fetching prices and exchange rates..."):
    df["Price"] = df["Symbol"].apply(get_price)
    df["FX Rate"] = df["Currency"].apply(get_fx_to_thb)
    df["Value (Local)"] = df["Shares"] * df["Price"]
    df["Value (THB)"] = df["Value (Local)"] * df["FX Rate"]
    total_thb = df["Value (THB)"].sum()
    df["Weight (%)"] = (df["Value (THB)"] / total_thb * 100).round(2)

# Display portfolio breakdown
st.subheader("📄 Portfolio Breakdown")
st.dataframe(df[["Symbol", "Shares", "Currency", "Price", "Value (Local)", "FX Rate", "Value (THB)", "Weight (%)"]])

# Show total value in THB
st.metric("💰 Total Portfolio Value (THB)", f"฿{total_thb:,.2f}")

# Pie chart by THB allocation
st.subheader("📈 Allocation Pie Chart (THB)")
fig, ax = plt.subplots()
df.set_index("Symbol")["Weight (%)"].plot.pie(
    autopct='%1.1f%%', figsize=(5, 5), ylabel="", ax=ax
)
st.pyplot(fig)
