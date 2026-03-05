# user_preferences.py
import streamlit as st
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserPreference:
    sheet_url: Optional[str] = None        # original user input (optional)
    sheet_csv_url: Optional[str] = None    # final CSV export URL (optional)

    investment_weight: float = 0.50
    gold_weight_reserve: float = 0.20

    years_rebound: int = 3
    years_dividend: int = 5


def convert_to_csv_url(sheet_url: str) -> str:
    sheet_url = sheet_url.strip()
    if "/edit" in sheet_url:
        return sheet_url.split("/edit")[0] + "/export?format=csv"
    elif sheet_url.endswith("/export?format=csv"):
        return sheet_url
    else:
        raise ValueError("Invalid Google Sheet link format. Expected a link containing '/edit'.")


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

    cleaned_url = input_url.strip() if input_url else ""
    default_csv_url = st.secrets["google_sheet"]["url"]

    # Decide final CSV url
    try:
        sheet_csv_url = convert_to_csv_url(cleaned_url) if cleaned_url else default_csv_url
    except ValueError:
        st.sidebar.error("❌ Invalid link format. Please make sure it's a shared Google Sheet URL.")
        sheet_csv_url = default_csv_url

    # Investment allocation slider (user-friendly % input, returned as decimals)
    st.sidebar.markdown("### 🧑‍💼 Investment Mode: Risk-Off/On")
    investment_pct = st.sidebar.slider(
        label="Set Investment Portion (%)",
        min_value=25,
        max_value=75,
        value=50,
        step=1,
        help="Investment portion includes core, growth, and speculative assets."
    )
    gold_pct = st.sidebar.slider(
        label="Set Gold (%) of Reserve Portion",
        min_value=0,
        max_value=50,
        value=20,
        step=1,
        help="Reserve portion includes cash, bond, and gold."
    )

    # Assumption inputs
    st.sidebar.markdown("### 📉 Assumption")
    years_rebound = st.sidebar.number_input(
        "Years to Fully Rebound from MDD",
        value=3,
        min_value=1,
        max_value=10,
        step=1
    )
    years_dividend = st.sidebar.number_input(
        "Years for Dividend to cover MDD",
        value=5,
        min_value=1,
        max_value=10,
        step=1
    )

    # Convert % to decimals
    investment_weight = investment_pct / 100.0
    gold_weight_reserve = gold_pct / 100.0

    prefs = UserPreference(
        sheet_url=cleaned_url or None,
        sheet_csv_url=sheet_csv_url,
        investment_weight=investment_weight,
        gold_weight_reserve=gold_weight_reserve,
        years_rebound=int(years_rebound),
        years_dividend=int(years_dividend),
    )

    return prefs
