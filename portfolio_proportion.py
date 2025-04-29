#  portfolio_proportion.py

from asset_data import AssetData
from typing import List

def assign_targets(assets: List[AssetData], investment_pct: float):
    reserve_pct = 100 - investment_pct
    mdd_investment_pct = 9.3  # Based on your table: MDD ≈ 9.3% for investment portfolio

    # Calculate allocations
    cash_pct = mdd_investment_pct * investment_pct / 100
    gold_pct = 0.2 * reserve_pct
    bond_pct = reserve_pct - cash_pct - gold_pct

    reserve_allocation = {
        "Cash": cash_pct,
        "Bond": bond_pct,
        "Gold": gold_pct,
    }

    investment_allocation = {
        "Core": 0.6 * investment_pct,
        "Growth": 0.3 * investment_pct,
        "Speculative": 0.1 * investment_pct,
    }

    # --- Count number of assets for each type ---
    type_counts = {}
    for asset in assets:
        if asset.asset_type:
            type_counts[asset.asset_type] = type_counts.get(asset.asset_type, 0) + 1

    # --- Assign target percentage per asset ---
    for asset in assets:
        if asset.asset_type in reserve_allocation:
            count = type_counts[asset.asset_type]
            if count > 0:
                asset.target = reserve_allocation[asset.asset_type] / count / 100
            else:
                asset.target = 0
        elif asset.asset_type in investment_allocation:
            count = type_counts[asset.asset_type]
            if count > 0:
                asset.target = investment_allocation[asset.asset_type] / count / 100
            else:
                asset.target = 0
        else:
            asset.target = 0  # Unknown type fallback

    return assets
