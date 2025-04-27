# portfolio_view.py

import pandas as pd
from asset_data import AssetData
from typing import List

def get_individual_df(assets: List[AssetData]) -> pd.DataFrame:
    return pd.DataFrame([{
        "name": asset.name,
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
        "weight": bond_df["weight"].sum(),
        "target": bond_df["target"].sum(),
        "type": "Bond"
    }

    cash_row = {
        "name": "Total Cash",
        "weight": cash_df["weight"].sum(),
        "target": cash_df["target"].sum(),
        "type": "Cash"
    }

    # Append totals at bottom
    summarized_df = pd.concat([others_df, pd.DataFrame([bond_row, cash_row])], ignore_index=True)
    return summarized_df
