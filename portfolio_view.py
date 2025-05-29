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
        "currency": asset.currency,
        "shares": asset.shares,
        "price": asset.price,
        "fx rate": asset.fx_rate,
        "value (thb)": asset.value_thb,
        "type": asset.asset_type,
        "weight": asset.weight,
        "target": asset.target,
        "%drift": asset.drift_pct,
        "position": asset.position_size,
        "52w high": asset.high_52w,
        "52w low": asset.low_52w,
        "drop_1y": asset.drop_1y,
        "gain_1y": asset.gain_1y,
        "gain_3y": asset.gain_3y,
        "price_change": asset.price_change,
        "pe": asset.pe_ratio,
        "pe_p25": asset.pe_p25,
        "pe_p75": asset.pe_p75,
        "pe_signal": asset.pe_signal,
        "yield": asset.dividend_yield,
    } for asset in assets])

def show_portfolio_table(portfolio_df: pd.DataFrame):
    st.subheader("📋 Portfolio Report")
    show_cols = ["name", "currency", "shares", "price", "fx rate", "value (thb)", "weight"]
    format_dict = {
        "shares": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "price": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "fx rate": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "value (thb)": lambda x: f"{x:,.0f}" if x != 0.0 else "-",
        "weight": lambda x: f"{x * 100:.1f}%" if x is not None else "-",
    }
    st.dataframe(portfolio_df[show_cols].style.format(format_dict))

def show_market_data_table(portfolio_df: pd.DataFrame):
    st.subheader("💹 Market Data")
    st.caption("ℹ️ Fetchable data. When using live data mode, copy this data to your Google Sheet to update static data.")
    show_cols = ["name", "currency", "price", "fx rate", "52w high", "52w low", "pe", "yield"]
    format_dict = {
        "price": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "fx rate": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "52w high": lambda x: f"{x:,.2f}" if x else "-",
        "52w low": lambda x: f"{x:,.2f}" if x else "-",
        "pe": lambda x: f"{x:,.0f}" if pd.notnull(x) and x != 0.0 else "-",
        "yield": lambda x: f"{x * 100:.1f}%" if x not in [None, 0.0] else "-",
    }
    st.dataframe(portfolio_df[show_cols].style.format(format_dict))

def show_summary_signal_table(portfolio_df: pd.DataFrame):
    st.subheader("📈 Portfolio Signals")
    
    show_cols = ["name", "type", "weight", "position", "price_change", "pe_signal", "yield"]
    format_dict = {
        "weight": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "yield": lambda x: f"{x * 100:.1f}%" if x not in [None, 0.0] else "-",
    }
    # Color Green and Red Format
    def highlight_condition(val):
        if str(val).lower() in ("oversize", "overbought", "overvalue"):
            return "color: red;"
        elif str(val).lower() in ("undersize", "oversold", "undervalue"):
            return "color: green;"
        return ""

    styled_df = (
        portfolio_df[show_cols]
        .style
        .format(format_dict)
        .applymap(highlight_condition, subset=["position", "price_change", "pe_signal"])
    )
    st.dataframe(styled_df)

def show_full_details_signal_table(portfolio_df: pd.DataFrame):
    st.subheader("🧮 Signal Calculations")
    
    show_cols = ["name", "type", "weight", "target", "%drift", "position", "drop_1y", "gain_1y", "gain_3y", "price_change", "pe", "pe_p25", "pe_p75", "pe_signal", "yield"]
    format_dict = {
        "weight": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "target": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "%drift": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "drop_1y": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "gain_1y": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "gain_3y": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "pe": lambda x: f"{x:,.0f}" if pd.notnull(x) and x != 0.0 else "-",
        "pe_p25": lambda x: f"{x:,.0f}" if pd.notnull(x) and x != 0.0 else "-",
        "pe_p75": lambda x: f"{x:,.0f}" if pd.notnull(x) and x != 0.0 else "-",
        "yield": lambda x: f"{x * 100:.1f}%" if x not in [None, 0.0] else "-",
    }
    # Color Green and Red Format
    def highlight_condition(val):
        if str(val).lower() in ("oversize", "overbought", "overvalue"):
            return "color: red;"
        elif str(val).lower() in ("undersize", "oversold", "undervalue"):
            return "color: green;"
        return ""

    styled_df = (
        portfolio_df[show_cols]
        .style
        .format(format_dict)
        .applymap(highlight_condition, subset=["position", "price_change", "pe_signal"])
    )
    st.dataframe(styled_df)

def show_allocation_pie_chart(portfolio_df: pd.DataFrame, total_thb: float):
    st.subheader("📊 Actual Allocation Pie Chart")

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

    # Drop NaN and filter out targets < 1%
    target_df = target_df.dropna(subset=["target"])
    target_df = target_df[target_df["target"] >= 0.01]

    target_df["target (%)"] = (target_df["target"] * 100).round(1)

    if target_df.empty:
        st.info("No assets with target allocation ≥ 1% to display.")
        return

    fig, ax = plt.subplots()
    target_df.set_index("name")["target (%)"].plot.pie(
        autopct="%1.0f%%",
        figsize=(5, 5),
        ylabel="",
        ax=ax
    )
    st.pyplot(fig)


