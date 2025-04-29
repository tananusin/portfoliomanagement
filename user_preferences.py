#user_preferences.py

import streamlit as st

def get_user_preferences() -> float:
    st.sidebar.header("User Preference")

    # Investment % Slider
    st.sidebar.markdown("### 🎯 Investment Mode: Risk-Off/Risk-On")
    investment_pct = st.sidebar.slider(
        label="Set Investment Portion (%)",
        min_value=25,
        max_value=75,
        value=50,
        step=1,
        help="Investment portion are Core, Growth, and Speculative assets. Reserve portion are Cash, Bond, and Gold."
    )
    return investment_pct
