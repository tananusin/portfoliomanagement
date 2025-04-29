# portfolio_view.py

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from asset_data import AssetData
from typing import List

def get_user_preferences() -> float:
    st.sidebar.header("User Preference")
    
    st.sidebar.markdown("### 🎯 Investment Mode")
    # Custom min/max labels
    col1, col2 = st.sidebar.columns(2)
    with col1: st.markdown("<div style='text-align: left;'>Risk-Off</div>", unsafe_allow_html=True)
    with col2: st.markdown("<div style='text-align: right;'>Risk-On</div>", unsafe_allow_html=True)
    # Investment % Slider
    investment_pct = st.sidebar.slider(
        label="Set Investment Portion (%)",
        min_value=25, max_value=75, value=50, step=1,
        help="Investment portion are Core, Growth, and Speculative assets. Reserve portion are Cash, Bond, and Gold."
    )
    return investment_pct

def get_portfolio_df(assets: List[AssetData]) -> pd.DataFrame:
    return pd.DataFrame([{
        "name": asset.name,
        "symbol": asset.symbol,
        "value (thb)": asset.value_thb,
        "type": asset.asset_type,
        "weight": asset.weight,
        "target": asset.target
    } for asset in assets])

def show_portfolio_table(portfolio_df: pd.DataFrame):
    st.subheader("📋 Portfolio Breakdown")
    
    show_cols = ["name", "type", "weight", "target"]
    format_dict = {
        "weight": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "target": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
    }
    st.dataframe(portfolio_df[show_cols].style.format(format_dict))

def show_allocation_pie_chart(portfolio_df: pd.DataFrame, total_thb: float):
    st.subheader("📈 Allocation Pie Chart")

    chart_df = portfolio_df[["name", "value (thb)"]].copy()
    chart_df["weight (%)"] = (chart_df["value (thb)"] / total_thb * 100).round(2)
    chart_df = chart_df[chart_df["weight (%)"] >= 1]

    fig, ax = plt.subplots()
    chart_df.set_index("name")["weight (%)"].plot.pie(
        autopct="%1.0f%%",
        figsize=(5, 5),
        ylabel="",
        ax=ax
    )
    st.pyplot(fig)
