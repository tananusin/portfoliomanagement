# portfolio_view.py

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from asset_data import AssetData
from typing import List

def get_portfolio_df(assets: List[AssetData]) -> pd.DataFrame:
    return pd.DataFrame([{
        "Name": asset.name,
        "Symbol": asset.symbol,
        "Currency": asset.currency,
        "Shares": asset.shares,
        "Price": asset.price,
        "Fx": asset.fx_rate,
        "Value (THB)": asset.value_thb,
        "Type": asset.asset_type,
        "Weight": asset.weight,
        "Target": asset.target,
        "%drift": asset.drift_pct,
        "Position": asset.position_size,
        "52w_high": asset.high_52w,
        "52w_low": asset.low_52w,
        "3y_low": asset.low_3y,
        "drop_1y": asset.drop_1y,
        "gain_1y": asset.gain_1y,
        "gain_3y": asset.gain_3y,
        "Price Change": asset.price_change,
        "PE": asset.pe_ratio,
        "PE_p25": asset.pe_p25,
        "PE_p75": asset.pe_p75,
        "PE Signal": asset.pe_signal,
        "Yield": asset.dividend_yield,
        "yield_offset": asset.dividend_yield_offset,
        "Yield Signal": asset.dividend_yield_signal,
    } for asset in assets])

def show_portfolio_table(portfolio_df: pd.DataFrame):
    st.subheader("📋 Portfolio Report")
    show_cols = ["Name", "Currency", "Shares", "Price", "Fx", "Value (THB)", "Weight"]
    format_dict = {
        "Shares": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "Price": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "Fx": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "Value (THB)": lambda x: f"{x:,.0f}" if x != 0.0 else "-",
        "Weight": lambda x: f"{x * 100:.1f}%" if x is not None else "-",
    }
    st.dataframe(portfolio_df[show_cols].style.format(format_dict))

def show_market_data_table(portfolio_df: pd.DataFrame):
    st.subheader("💹 Market Data")
    st.caption("ℹ️ Fetchable data. When using live data mode, copy this data to your Google Sheet to update static data.")
    show_cols = ["Name", "Currency", "Price", "Fx", "52w_high", "52w_low", "PE", "Yield"]
    format_dict = {
        "Price": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "Fx": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "52w_high": lambda x: f"{x:,.2f}" if x else "-",
        "52w_low": lambda x: f"{x:,.2f}" if x else "-",
        "PE": lambda x: f"{x:,.0f}" if pd.notnull(x) and x != 0.0 else "-",
        "Yield": lambda x: f"{x * 100:.1f}%" if x not in [None, 0.0] else "-",
    }
    st.dataframe(portfolio_df[show_cols].style.format(format_dict))

def show_summary_signal_table(portfolio_df: pd.DataFrame):
    st.subheader("📈 Portfolio Signals")
    
    show_cols = ["Name", "Type", "Weight", "Target", "Position", "Price Change", "PE Signal", "Yield Signal"]
    format_dict = {
        "Weight": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "Target": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
    }
    # Color Green and Red Format
    def highlight_condition(val):
        if str(val).lower() in ("oversize", "overbought", "overvalue"):
            return "color: red;"
        elif str(val).lower() in ("undersize", "oversold", "undervalue", "sufficient"):
            return "color: green;"
        return ""

    styled_df = (
        portfolio_df[show_cols]
        .style
        .format(format_dict)
        .applymap(highlight_condition, subset=["Position", "Price Change", "PE Signal", "Yield Signal"])
    )
    st.dataframe(styled_df)

def show_full_details_signal_table(portfolio_df: pd.DataFrame):
    st.subheader("🧮 Signal Calculations")
    
    show_cols = ["Name", "Type", "Weight", "Target", "%drift", "Position", "drop_1y", "gain_1y", "gain_3y", "Price Change", "PE", "PE_p25", "PE_p75", "PE Signal", "Yield", "yield_offset", "Yield Signal"]
    format_dict = {
        "Weight": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "Target": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "%drift": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "drop_1y": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "gain_1y": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "gain_3y": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "PE": lambda x: f"{x:,.0f}" if pd.notnull(x) and x != 0.0 else "-",
        "PE_p25": lambda x: f"{x:,.0f}" if pd.notnull(x) and x != 0.0 else "-",
        "PE_p75": lambda x: f"{x:,.0f}" if pd.notnull(x) and x != 0.0 else "-",
        "Yield": lambda x: f"{x * 100:.1f}%" if x not in [None, 0.0] else "-",
        "yield_offset": lambda x: f"{x * 100:.1f}%" if x not in [None, 0.0] else "-",
    }
    # Color Green and Red Format
    def highlight_condition(val):
        if str(val).lower() in ("oversize", "overbought", "overvalue"):
            return "color: red;"
        elif str(val).lower() in ("undersize", "oversold", "undervalue", "sufficient"):
            return "color: green;"
        return ""

    styled_df = (
        portfolio_df[show_cols]
        .style
        .format(format_dict)
        .applymap(highlight_condition, subset=["Position", "Price Change", "PE Signal", "Yield Signal"])
    )
    st.dataframe(styled_df)

def show_allocation_pie_chart(portfolio_df: pd.DataFrame, total_thb: float):
    st.subheader("📊 Actual Allocation Pie Chart")

    chart_df = portfolio_df[["Name", "Value (THB)"]].copy()
    chart_df["weight (%)"] = (chart_df["Value (THB)"] / total_thb * 100).round(2)
    chart_df = chart_df[chart_df["weight (%)"] >= 1]

    fig, ax = plt.subplots()
    chart_df.set_index("Name")["weight (%)"].plot.pie(
        autopct="%1.0f%%",
        figsize=(5, 5),
        ylabel="",
        ax=ax
    )
    st.pyplot(fig)

def show_target_allocation_pie_chart(portfolio_df: pd.DataFrame):
    st.subheader("🎯 Target Allocation Pie Chart")

    target_df = portfolio_df[["Name", "Target"]].copy()

    # Drop NaN and filter out targets < 1%
    target_df = target_df.dropna(subset=["Target"])
    target_df = target_df[target_df["Target"] >= 0.01]

    target_df["target (%)"] = (target_df["Target"] * 100).round(1)

    if target_df.empty:
        st.info("No assets with target allocation ≥ 1% to display.")
        return

    fig, ax = plt.subplots()
    target_df.set_index("Name")["target (%)"].plot.pie(
        autopct="%1.0f%%",
        figsize=(5, 5),
        ylabel="",
        ax=ax
    )
    st.pyplot(fig)


