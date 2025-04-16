# main.py
import streamlit as st
import pandas as pd
from fetch import get_price

st.set_page_config(page_title="Stock Portfolio", layout="centered")

st.title("📊 Live Stock Portfolio")

# Google Sheet CSV link (from your shared sheet)
sheet_url = "https://docs.google.com/spreadsheets/d/1T8H0By9mCahSaG09NOvc4bXGE_cDtDdCMsFoIabDCnw/export?format=csv"

# Load portfolio data
try:
    df = pd.read_csv(sheet_url)
except Exception as e:
    st.error("❌ Failed to load Google Sheet.")
    st.stop()

# Fetch prices and compute values
with st.spinner("Fetching live prices..."):
    df["Price"] = df["Symbol"].apply(get_price)
    df["Value"] = df["Shares"] * df["Price"]
    total_value = df["Value"].sum()
    df["Weight (%)"] = (df["Value"] / total_value * 100).round(2)

# Show table
st.subheader("📋 Portfolio Breakdown")
st.dataframe(df)

import matplotlib.pyplot as plt  # Add at the top if not already

# Pie chart
st.subheader("📈 Allocation Pie Chart")
fig, ax = plt.subplots()
df.set_index("Symbol")["Weight (%)"].plot.pie(
    autopct='%1.1f%%',
    figsize=(5, 5),
    ylabel='',
    ax=ax
)
st.pyplot(fig)

# Total value
st.metric("💰 Total Portfolio Value", f"${total_value:,.2f}")
