# debug_view.py

import pandas as pd
import streamlit as st


def show_debug_table(portfolio_df: pd.DataFrame):
    show_cols = [
        "Name", "MDD", "Rebound", "CAGR", "Offset Yield", 
        "Inverse MDD", "Target in Class", "Target", "MDD Contribution",
    ]

    format_dict = {
        "MDD": lambda x: f"{x * 100:.0f}%" if x not in [None, 0.0] else "-",
        "Rebound": lambda x: f"{x * 100:.0f}%" if x not in [None, 0.0] else "-",
        "CAGR": lambda x: f"{x * 100:.0f}%" if x not in [None, 0.0] else "-",
        "Offset Yield": lambda x: f"{x * 100:.0f}%" if x not in [None, 0.0] else "-",
        "Inverse MDD": lambda x: f"{x:,.2f}" if x not in [None, 0.0] else "-",
        "Target in Class": lambda x: f"{x * 100:.0f}%" if x not in [None, 0.0] else "-",
        "Target": lambda x: f"{x * 100:.0f}%" if x not in [None, 0.0] else "-",
        "MDD Contribution": lambda x: f"{x * 100:.0f}%" if x not in [None, 0.0] else "-",
    }

    st.dataframe(
        portfolio_df[show_cols].style.format(format_dict),
        use_container_width=True,
    )


def show_risk_class_table(risk_classes):
    data = []

    for rc in risk_classes:
        data.append({
            "Class": rc.name,
            "Class MDD": rc.class_mdd,
            "Inverse MDD": rc.class_mdd_inverse,
            "Target Weight": rc.class_target_weight,
            "Risk Contribution": rc.class_mdd_contribution,
        })

    df = pd.DataFrame(data)

    if "Class MDD" in df:
        df["Class MDD"] = df["Class MDD"].map(
            lambda x: f"{x:.0%}" if pd.notnull(x) else ""
        )
    if "Target Weight" in df:
        df["Target Weight"] = df["Target Weight"].map(
            lambda x: f"{x:.0%}" if pd.notnull(x) else ""
        )
    if "Risk Contribution" in df:
        df["Risk Contribution"] = df["Risk Contribution"].map(
            lambda x: f"{x:.0%}" if pd.notnull(x) else ""
        )
    if "Inverse MDD" in df:
        df["Inverse MDD"] = df["Inverse MDD"].map(
            lambda x: f"{x:.2f}" if pd.notnull(x) else ""
        )

    st.dataframe(df, use_container_width=True)

def show_currency_table(currencies):
    data = []

    for ccy in currencies:
        data.append({
            "Currency": ccy.name,
            "Investment Weight": ccy.currency_investment_weight,
            "Investment MDD": ccy.currency_investment_mdd,
            "Cash Weight": ccy.currency_cash_weight,
            "Cash Ratio": ccy.currency_cash_ratio,
            "Bond Weight": ccy.currency_bond_weight,
        })

    df = pd.DataFrame(data)

    if "Investment Weight" in df:
        df["Investment Weight"] = df["Investment Weight"].map(
            lambda x: f"{x:.1%}" if pd.notnull(x) else ""
        )
    if "Investment MDD" in df:
        df["Investment MDD"] = df["Investment MDD"].map(
            lambda x: f"{x:.1%}" if pd.notnull(x) else ""
        )
    if "Cash Weight" in df:
        df["Cash Weight"] = df["Cash Weight"].map(
            lambda x: f"{x:.1%}" if pd.notnull(x) else ""
        )
    if "Cash Ratio" in df:
        df["Cash Ratio"] = df["Cash Ratio"].map(
            lambda x: f"{x:.1%}" if pd.notnull(x) else ""
        )
    if "Bond Weight" in df:
        df["Bond Weight"] = df["Bond Weight"].map(
            lambda x: f"{x:.1%}" if pd.notnull(x) else ""
        )

    st.dataframe(df, use_container_width=True)
