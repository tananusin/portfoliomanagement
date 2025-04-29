# portfolio_view.py

import pandas as pd
from asset_data import AssetData
from typing import List

def get_individual_df(assets: List[AssetData]) -> pd.DataFrame:
    return pd.DataFrame([{
        "name": asset.name,
        "symbol": asset.symbol,
        "value (thb)": asset.value_thb,
        "weight": asset.weight,
        "type": asset.asset_type
    } for asset in assets])
