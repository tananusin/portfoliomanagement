# user_preferences.py

import streamlit as st
from dataclasses import dataclass

@dataclass
class UserPreference:
    investment_pct: int
    password: str

def get_user_preferences() -> UserPreference:
    st.sidebar.header("User Preference")

    # Password input for accessing real-time data
    password = st.sidebar.text_input(
        "🔑 Enter password for live data access:",
        type="password"
    )

    # Investment slider
    st.sidebar.markdown("### 🎯 Investment Mode: Risk-Off/Risk-On")
    investment_pct = st.sidebar.slider(
        label="Set Investment Portion (%)",
        min_value=25,
        max_value=75,
        value=50,
        step=1,
        help="Investment portion includes Core, Growth, and Speculative assets. Reserve portion includes Cash, Bond, and Gold."
    )

    return UserPreference(
        investment_pct=investment_pct,
        password=password
    )

