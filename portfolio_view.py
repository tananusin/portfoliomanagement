# portfolio_view.py

import pandas as pd
from asset_data import AssetData
from typing import List

def get_individual_df(assets: List[AssetData]) -> pd.DataFrame:
    return pd.DataFrame([{
        "name": asset.name,
        "symbol": asset.symbol,
        "currency": asset.currency,
        "shares": asset.shares,
        "price": asset.price,
        "fx rate": asset.fx_rate,
        "value (thb)": asset.value_thb,
        "weight": asset.weight,
        "target": asset.target,
        "type": asset.asset_type
    } for asset in assets])

def get_summarized_df(assets: List[AssetData]) -> pd.DataFrame:
    df = get_individual_df(assets)
    
    # Always uppercase to be safe
    df["symbol"] = df["symbol"].str.upper()

    # Summarize bond and cash
    bond_df = df[df["symbol"] == "BOND"]
    cash_df = df[df["symbol"] == "CASH"]
    others_df = df[~df["symbol"].isin(["BOND", "CASH"])]

    bond_row = {
        "name": "Total Bonds",
        "symbol": "BOND",
        "currency": "-",
        "shares": 0.0,
        "price": 0.0,
        "fx rate": 0.0,
        "value (thb)": bond_df["value (thb)"].sum(),
        "weight": bond_df["weight"].sum(),
        "target": bond_df["target"].sum(),
        "type": "Bond"
    }

    cash_row = {
        "name": "Total Cash",
        "symbol": "CASH",
        "currency": "-",
        "shares": 0.0,
        "price": 0.0,
        "fx rate": 0.0,
        "value (thb)": cash_df["value (thb)"].sum(),
        "weight": cash_df["weight"].sum(),
        "target": cash_df["target"].sum(),
        "type": "Cash"
    }

    # Append totals at bottom
    summarized_df = pd.concat([others_df, pd.DataFrame([bond_row, cash_row])], ignore_index=True)
    return summarized_df
