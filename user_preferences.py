#user_preferences.py

import streamlit as st

def get_user_preferences() -> float:
    st.sidebar.header("User Preference")
    st.sidebar.markdown("### 🎯 Investment Mode")

    # Custom min/max labels
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.markdown("<div style='text-align: left;'>Risk-Off</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='text-align: right;'>Risk-On</div>", unsafe_allow_html=True)

    # Investment % Slider
    investment_pct = st.sidebar.slider(
        label="Set Investment Portion (%)",
        min_value=25,
        max_value=75,
        value=50,
        step=1,
        help="Investment portion are Core, Growth, and Speculative assets. Reserve portion are Cash, Bond, and Gold."
    )

    return investment_pct
