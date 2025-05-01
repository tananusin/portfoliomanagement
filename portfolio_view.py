# portfolio_view.py

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from asset_data import AssetData
from typing import List

def get_portfolio_df(assets: List[AssetData]) -> pd.DataFrame:
    return pd.DataFrame([{
        "name": asset.name,
        "symbol": asset.symbol,
        "value (thb)": asset.value_thb,
        "type": asset.asset_type,
        "weight": asset.weight,
        "target": asset.target,
        "position": asset.position_size
    } for asset in assets])

def show_portfolio_table(portfolio_df: pd.DataFrame):
    st.subheader("📋 Portfolio Breakdown")
    
    show_cols = ["name", "type", "weight", "target", "position"]
    format_dict = {
        "weight": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "target": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "drift": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "drift_pct": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
    }
    # Color Green and Red Format
    def highlight_position(val):
        if val == "oversize":
            return "color: red;"
        elif val == "undersize":
            return "color: green;"
        return ""
    styled_df = (
        portfolio_df[show_cols]
        .style
        .format(format_dict)
        .applymap(highlight_position, subset=["position"])
    )
    st.dataframe(styled_df)

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

def show_target_allocation_pie_chart(portfolio_df: pd.DataFrame):
    st.subheader("🎯 Target Allocation Pie Chart")

    target_df = portfolio_df[["name", "target"]].copy()
    target_df = target_df[target_df["target"] > 0]  # Filter out 0 targets
    target_df["target (%)"] = (target_df["target"] * 100).round(1)

    fig, ax = plt.subplots()
    target_df.set_index("name")["target (%)"].plot.pie(
        autopct="%1.0f%%",
        figsize=(5, 5),
        ylabel="",
        ax=ax
    )
    st.pyplot(fig)
