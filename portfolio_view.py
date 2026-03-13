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
        "Class": asset.asset_class,
        "assumed MDD": asset.mdd,
        "MDD": asset.mdd,            #for debug table

        "Weight": asset.weight,
        
        "Rebound": asset.rebound,
        "CAGR": asset.cagr,
        "Offset Yield": asset.dividend_yield_offset,

        "Inverse MDD": asset.mdd_inverse,
        "Target in Class": asset.target_in_class,
        "Target": asset.target,
        "MDD Contribution": asset.mdd_contribution,
        
        "Drift": asset.drift,
        "%Drift": asset.drift_relative,
        "Position": asset.position_size,
    
        "52w high": asset.high_52w,
        "52w low": asset.low_52w,
        "Years low": asset.low_years,
        "52w drop": asset.drop_52w,
        "52w gain": asset.gain_52w,
        "Years gain": asset.gain_years,
        "Calmar ratio": asset.calmar_ratio,
        "Price Signal": asset.price_signal,
        
        "PE": asset.pe_ratio,
        "PE p25": asset.pe_p25,
        "PE p75": asset.pe_p75,
        "PE Signal": asset.pe_signal,
        
        "Yield": asset.dividend_yield,
        "Yield Signal": asset.dividend_yield_signal,
    } for asset in assets])

def show_portfolio_table(portfolio_df: pd.DataFrame):
    show_cols = ["Name", "Currency", "Shares", "Price", "Fx", "Value (THB)", "Weight"]
    format_dict = {
        "Shares": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "Price": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "Fx": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "Value (THB)": lambda x: f"{x:,.0f}" if x != 0.0 else "-",
        "Weight": lambda x: f"{x * 100:.1f}%" if x is not None else "-",
    }
    st.dataframe(portfolio_df[show_cols].style.format(format_dict))

def show_summary_signal_table(portfolio_df: pd.DataFrame):
    show_cols = ["Name", "Class", "Weight", "Target", "Position", "Price Signal", "PE Signal", "Yield Signal"]
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
        .applymap(highlight_condition, subset=["Position", "Price Signal", "PE Signal", "Yield Signal"])
    )
    st.dataframe(styled_df)

def show_position_table(portfolio_df: pd.DataFrame):
    show_cols = ["Name", "Class", "Weight", "Target", "Drift", "%Drift", "Position"]
    format_dict = {
        "Weight": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "Target": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "Drift": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "%Drift": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
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
        .applymap(highlight_condition, subset=["Position"])
    )
    st.dataframe(styled_df)

def show_price_signal_table(portfolio_df: pd.DataFrame):
    show_cols = ["Name", "Class", "assumed MDD", "52w drop", "52w gain", "Years gain", "Calmar ratio", "Price Signal"]
    format_dict = {
        "assumed MDD": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "52w drop": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "52w gain": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "Calmar ratio": lambda x: f"{x:,.2f}" if pd.notnull(x) and x != 0.0 else "-",
        "Years gain": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
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
        .applymap(highlight_condition, subset=["Price Signal"])
    )
    st.dataframe(styled_df)

def show_pe_signal_table(portfolio_df: pd.DataFrame):
    show_cols = ["Name", "Class","PE", "PE p25", "PE p75", "PE Signal"]
    format_dict = {
        "PE": lambda x: f"{x:,.0f}" if pd.notnull(x) and x != 0.0 else "-",
        "PE p25": lambda x: f"{x:,.0f}" if pd.notnull(x) and x != 0.0 else "-",
        "PE p75": lambda x: f"{x:,.0f}" if pd.notnull(x) and x != 0.0 else "-",
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
        .applymap(highlight_condition, subset=["PE Signal"])
    )
    st.dataframe(styled_df)

def show_yield_signal_table(portfolio_df: pd.DataFrame):
    show_cols = ["Name", "Class", "assumed MDD", "52w drop", "Yield", "Offset Yield", "Yield Signal"]
    format_dict = {
        "assumed MDD": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "52w drop": lambda x: f"{x * 100:.1f}%" if x not in (None, 0.0) else "-",
        "Yield": lambda x: f"{x * 100:.1f}%" if x not in [None, 0.0] else "-",
        "Offset Yield": lambda x: f"{x * 100:.1f}%" if x not in [None, 0.0] else "-",
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
        .applymap(highlight_condition, subset=["Yield Signal"])
    )
    st.dataframe(styled_df)

def show_google_sheet_data_table(portfolio_df: pd.DataFrame):
    show_cols = ["Name", "Symbol", "Currency", "Shares", "Price", "Fx", "Class", "assumed MDD", "52w high", "52w low", "Years low", "PE", "PE p25", "PE p75", "Yield"]
    format_dict = {
        "Shares": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "Price": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "assumed MDD": lambda x: f"{x * 100:.0f}%" if x not in [None, 0.0] else "-",
        "Fx": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "52w high": lambda x: f"{x:,.2f}" if x else "-",
        "52w low": lambda x: f"{x:,.2f}" if x else "-",
        "Years low": lambda x: f"{x:,.2f}" if x else "-",
        "PE": lambda x: f"{x:,.2f}" if pd.notnull(x) and x != 0.0 else "-",
        "PE p25": lambda x: f"{x:,.2f}" if pd.notnull(x) and x != 0.0 else "-",
        "PE p75": lambda x: f"{x:,.2f}" if pd.notnull(x) and x != 0.0 else "-",
        "Yield": lambda x: f"{x * 100:.2f}%" if x not in [None, 0.0] else "-",
    }
    st.dataframe(portfolio_df[show_cols].style.format(format_dict))

def show_allocation_pie_chart(portfolio_df: pd.DataFrame, total_thb: float):
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

