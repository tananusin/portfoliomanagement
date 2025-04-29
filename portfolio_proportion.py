#  portfolio_proportion.py

from asset_data import AssetData
from typing import List

def assign_targets(assets: List[AssetData], investment_pct: float):
    reserve_pct = 100 - investment_pct

    reserve_allocation = {
        "Cash": investment_pct,  # Cash = %MDD of investment = 9.3%
        "Bond": reserve_pct - investment_pct,  # Bond = excess reserve after Cash
        "Gold": 0.2 * reserve_pct,  # Gold = 20% of reserve
    }

    investment_allocation = {
        "Core": 0.6 * investment_pct,
        "Growth": 0.3 * investment_pct,
        "Speculative": 0.1 * investment_pct,
    }

    for asset in assets:
        if asset.asset_type in reserve_allocation:
            asset.target = reserve_allocation[asset.asset_type] / 100
        elif asset.asset_type in investment_allocation:
            asset.target = investment_allocation[asset.asset_type] / 100
        else:
            asset.target = 0  # For unknown types

    return assets
