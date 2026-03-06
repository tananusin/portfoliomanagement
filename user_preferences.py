# user_preferences.py
import streamlit as st
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserPreference:
    sheet_url: str

    investment_weight: float = 0.50
    gold_weight_reserve: float = 0.20

    years_rebound: int = 3
    years_dividend: int = 5
    
    threshold_drift: float = 0.05
    threshold_drift_relative: float = 0.50


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

    # Google Sheet URL input
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
        st.sidebar.error("❌ Invalid link format. Please make sure it's a shared Google Sheet URL.")
        sheet_url = st.secrets["google_sheet"]["url"]

    
    # Investment allocation slider (user-friendly % input, returned as decimals)
    st.sidebar.markdown("### 🧑‍💼 Investment Mode: Risk-Off/On")
    investment_pct = st.sidebar.slider(
        label="Set Investment Portfolio (%)",
        min_value=25,
        max_value=75,
        value=50,
        step=1,
        help="Investment portfolio includes core, growth, and speculative assets."
    )
    gold_pct = st.sidebar.slider(
        label="Set Gold (%) of Reserve Portfolio",
        min_value=0,
        max_value=50,
        value=20,
        step=1,
        help="Reserve portfolio includes cash, bond, and gold."
    )

    # Assumption inputs
    st.sidebar.markdown("### ⏳ Assumptions")
    years_rebound = st.sidebar.number_input(
        "Years for Prices to Fully Rebound from MDD",
        value=3,
        min_value=1,
        max_value=10,
        step=1
    )
    years_dividend = st.sidebar.number_input(
        "Years for Dividends to cover MDD",
        value=5,
        min_value=1,
        max_value=10,
        step=1
    )

    # Drift thresholds
    st.sidebar.markdown("### ⚖️ Rebalancing Thresholds")
    threshold_drift_pct = st.sidebar.number_input(
        "Absolute Drift Threshold (%)",
        value=5,
        min_value=1,
        max_value=10,
        step=1,
        help="Example: 5 means rebalance when weight differs from target by more than 5 percentage points."
    )
    threshold_drift_relative_pct = st.sidebar.number_input(
        "Relative Drift Threshold (%)",
        value=50,
        min_value=20,
        max_value=200,
        step=10,
        help="Example: 50 means rebalance when drift is more than 50% of target weight."
    )
    
    # Convert % to decimals
    investment_weight = investment_pct / 100
    gold_weight_reserve = gold_pct / 100
    threshold_drift = threshold_drift_pct / 100
    threshold_drift_relative = threshold_drift_relative_pct / 100

    prefs = UserPreference(
        sheet_url=sheet_url,
        investment_weight=investment_weight,
        gold_weight_reserve=gold_weight_reserve,
        years_rebound=int(years_rebound),
        years_dividend=int(years_dividend),
        threshold_drift=threshold_drift,
        threshold_drift_relative=threshold_drift_relative,
    )

    return prefs
