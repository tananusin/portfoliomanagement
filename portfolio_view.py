# portfolio_view.py

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from asset_data import AssetData
from typing import List

def get_individual_df(assets: List[AssetData]) -> pd.DataFrame:
    return pd.DataFrame([{
        "name": asset.name,
        "symbol": asset.symbol,
        "value (thb)": asset.value_thb,
        "type": asset.asset_type,
        "weight": asset.weight,
        "target": asset.target
    } for asset in assets])

def show_portfolio_table(portfolio_df: pd.DataFrame):
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
