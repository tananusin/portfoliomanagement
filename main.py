import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fetch import get_price, get_fx_to_thb
from positionsize import classify_position  # Import the new function

st.set_page_config(page_title="Portfolio Rebalancer", layout="centered")
st.title("📊 Portfolio Rebalancer")

# Access the Google Sheets URL from Streamlit secrets
sheet_url = st.secrets["google_sheet"]["url"]

# Load and clean data
try:
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip().str.lower()
except Exception as e:
    st.error(f"❌ Failed to load Google Sheet: {e}")
    st.stop()

# Validate columns
required_cols = {"name", "symbol", "currency", "shares", "target"}
if not required_cols.issubset(df.columns):
    st.error(f"Missing columns in Google Sheet. Required: {required_cols}")
    st.write("Loaded columns:", df.columns.tolist())
    st.stop()

# Fetch price and FX
with st.spinner("Fetching live prices and FX rates..."):
    df["price"] = df["symbol"].apply(get_price)
    df["fx rate"] = df["currency"].apply(get_fx_to_thb)
    df["value (local)"] = df["shares"] * df["price"]
    df["value (thb)"] = df["value (local)"] * df["fx rate"]

# Total portfolio value in THB
total_thb = df["value (thb)"].sum()
df["weight"] = (df["value (thb)"] / total_thb).round(4)

# Convert 'target' %string to numbers
df["target"] = pd.to_numeric(
    df["target"].astype(str).str.replace(r"[^\d.]+", "", regex=True),
    errors="coerce"
) / 100

# Classify each position (oversized, undersized, aligned) based on target and weight
df[["position", "drift"]] = df.apply(
    lambda row: pd.Series(classify_position(row["weight"], row["target"])),
    axis=1
)

# Portfolio Table with formatted numbers
st.subheader("📄 Portfolio Breakdown")
show_cols = ["name", "currency", "shares", "price", "fx rate", "value (thb)", "weight"", "position"]
format_dict = {
    "shares": "{:,.2f}",
    "price": "{:,.2f}",
    "fx rate": "{:,.2f}",
    "value (thb)": "{:,.0f}",
    "weight": lambda x: f"{x * 100:.0f}%",
}
st.dataframe(df[show_cols].style.format(format_dict))

# Show total portfolio value
st.metric("💰 Total Portfolio Value (THB)", f"฿{total_thb:,.0f}")

# Prepare Pie Chart: Group all cash rows together
cash_mask = df["symbol"].str.upper().str.startswith("CASH")
cash_df = df[cash_mask]
non_cash_df = df[~cash_mask]

# Summarize cash as a single row
if not cash_df.empty:
    cash_value = cash_df["value (thb)"].sum()
    cash_row = pd.DataFrame([{
        "name": "Cash",
        "value (thb)": cash_value
    }])
    chart_df = pd.concat([non_cash_df[["name", "value (thb)"]], cash_row], ignore_index=True)
else:
    chart_df = non_cash_df[["name", "value (thb)"]]

# Compute weight for chart
chart_df["weight (%)"] = (chart_df["value (thb)"] / total_thb * 100).round(2)

# Pie Chart
st.subheader("📈 Allocation Pie Chart")
fig, ax = plt.subplots()
chart_df.set_index("name")["weight (%)"].plot.pie(
    autopct="%1.0f%%", figsize=(5, 5), ylabel="", ax=ax
)
st.pyplot(fig)
