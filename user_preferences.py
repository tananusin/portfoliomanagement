# user_preferences.py

import streamlit as st
from dataclasses import dataclass
from typing import Optional

@dataclass
class UserPreference:
    investment_pct: int
    password: str
    mdd_speculative_pct: int
    mdd_growth_pct: int
    mdd_core_pct: int

    cagr_speculative_pct: Optional[float] = None
    cagr_growth_pct: Optional[float] = None
    cagr_core_pct: Optional[float] = None 
    recover_speculative: Optional[float] = None
    recover_growth: Optional[float] = None
    recover_core: Optional[float] = None

    def compute_growth_metrics(self):
        def calc(mdd_pct: int):
            recovery = 1 / (1 + mdd_pct / 100)
            cagr = recovery ** (1 / 3) - 1
            return round(cagr * 100, 2), round(recovery, 2)

        self.cagr_speculative_pct, self.recover_speculative = calc(self.mdd_speculative_pct)
        self.cagr_growth_pct, self.recover_growth = calc(self.mdd_growth_pct)
        self.cagr_core_pct, self.recover_core = calc(self.mdd_core_pct)

def get_user_preferences() -> UserPreference:
    st.sidebar.header("🛠️ User Preference")

    # Password input
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
        help="Investment portion includes Core, Growth, and Speculative assets. Reserve portion includes Cash, Bond, and Gold."
    )

    # MDD inputs
    st.sidebar.markdown("### 📉 Maximum Drawdown (%)")
    mdd_speculative_pct = st.sidebar.number_input(
        "Speculative Assets", value=-75, min_value=-99, max_value=-1, step=1
    )
    mdd_growth_pct = st.sidebar.number_input(
        "Growth Assets", value=-50, min_value=-99, max_value=-1, step=1
    )
    mdd_core_pct = st.sidebar.number_input(
        "Core Assets", value=-25, min_value=-99, max_value=-1, step=1
    )

    return UserPreference(
        investment_pct=investment_pct,
        password=password,
        mdd_speculative_pct=mdd_speculative_pct,
        mdd_growth_pct=mdd_growth_pct,
        mdd_core_pct=mdd_core_pct
    )


