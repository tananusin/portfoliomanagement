# user_preferences.py
import streamlit as st
from dataclasses import dataclass
from typing import Optional

@dataclass
class UserPreference:
    investment_pct: int
    gold_pct: int
    password: str
    sheet_url: str
    mdd_speculative_pct: int
    mdd_growth_pct: int
    mdd_core_pct: int

    cagr_speculative_pct: Optional[float] = None
    cagr_growth_pct: Optional[float] = None
    cagr_core_pct: Optional[float] = None 
    rebound_speculative_pct: Optional[float] = None
    rebound_growth_pct: Optional[float] = None
    rebound_core_pct: Optional[float] = None

    yield_speculative: Optional[float] = None
    yield_growth: Optional[float] = None
    yield_core: Optional[float] = None 
    
    def compute_growth_metrics(self):
        def calc(mdd_pct: int):
            rebound_multiplier = 1 / (1 + mdd_pct / 100)
            cagr = rebound_multiplier ** (1 / 3) - 1
            rebound_pct = (rebound_multiplier - 1) * 100
            return round(cagr * 100, 2), round(rebound_pct, 2)

        self.cagr_speculative_pct, self.rebound_speculative_pct = calc(self.mdd_speculative_pct)
        self.cagr_growth_pct, self.rebound_growth_pct = calc(self.mdd_growth_pct)
        self.cagr_core_pct, self.rebound_core_pct = calc(self.mdd_core_pct)
    
    def compute_yield_metrics(self):
        self.yield_speculative = (self.mdd_speculative_pct)/-5
        self.yield_growth = (self.mdd_growth_pct)/-5
        self.yield_core = (self.mdd_core_pct)/-5


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

    st.sidebar.markdown("### 🔑 Switch to Live Data")
    password = st.sidebar.text_input(
        "Enter password for live data access:",
        type="password"
    )
    
    # Investment allocation slider
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

    # MDD inputs
    st.sidebar.markdown("### 📉 Maximum Drawdown (%MDD)")
    mdd_core_pct = st.sidebar.number_input(
        "Core Assets", value=-25, min_value=-95, max_value=-5, step=5
    )
    mdd_growth_pct = st.sidebar.number_input(
        "Growth Assets", value=-50, min_value=-95, max_value=-5, step=5
    )
    mdd_speculative_pct = st.sidebar.number_input(
        "Speculative Assets", value=-70, min_value=-95, max_value=-5, step=5
    )

    # Create UserPreference object
    prefs = UserPreference(
        investment_pct=investment_pct,
        gold_pct=gold_pct,
        password=password,
        sheet_url=sheet_url,
        mdd_speculative_pct=mdd_speculative_pct,
        mdd_growth_pct=mdd_growth_pct,
        mdd_core_pct=mdd_core_pct
    )
    prefs.compute_growth_metrics()
    prefs.compute_yield_metrics()

    # Display price rebound metrics
    st.sidebar.markdown("### 📈 Price Growth Rate")
    st.sidebar.caption("ℹ️ Assumes price rebounds from MDD in 3 yrs.")
    st.sidebar.write(f"Core: rebound {round(prefs.rebound_core_pct)}% → CAGR {round(prefs.cagr_core_pct)}%")
    st.sidebar.write(f"Growth: rebound {round(prefs.rebound_growth_pct)}% → CAGR {round(prefs.cagr_growth_pct)}%")
    st.sidebar.write(f"Speculative: rebound {round(prefs.rebound_speculative_pct)}% → CAGR {round(prefs.cagr_speculative_pct)}%")

    # Display dividend yield metrics
    st.sidebar.markdown("### 💵 Dividend Yield")
    st.sidebar.caption("ℹ️ Expects dividend to offset MDD loss in 5 yrs.")
    st.sidebar.write(f"Core: yield {round(prefs.yield_core)}%")
    st.sidebar.write(f"Growth: yield {round(prefs.yield_growth)}%")
    st.sidebar.write(f"Speculative: yield {round(prefs.yield_speculative)}%")
    
    return prefs

