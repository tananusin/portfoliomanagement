# portfolio_proportion.py

from asset_data import AssetData
from typing import List

# --- Fixed Asset %MDD ---
ACCEPTABLE_MDD = {
    "Core": -25,
    "Growth": -50,
    "Speculative": -70,
}

# --- Fixed Investment Allocation ---
INVESTMENT_ALLOCATION = {
    "Core": 0.6,         # 60% of investment
    "Growth": 0.3,       # 30% of investment
    "Speculative": 0.1,  # 10% of investment
}

# --- Functions ---
def calculate_investment_mdd(investment_pct: float) -> float:
    mdd_investment = 0
    for asset_type, mdd in ACCEPTABLE_MDD.items():
        alloc = INVESTMENT_ALLOCATION.get(asset_type, 0)
        mdd_investment += mdd * alloc * investment_pct / 100
    return abs(mdd_investment)  # Positive %

def assign_targets(assets: List[AssetData], investment_pct: float):
    reserve_pct = 100 - investment_pct

    # Correct dynamic calculation
    mdd_investment = calculate_investment_mdd(investment_pct)

    # Calculate reserve allocation
    cash_pct = mdd_investment * investment_pct / 100
    gold_pct = 0.2 * reserve_pct    # Fixed Gold 20% Reserve Allocation
    bond_pct = reserve_pct - cash_pct - gold_pct

    if bond_pct < 0:
        cash_pct += bond_pct  # reduce cash by overshoot
        bond_pct = 0.0        # set bond to 0
    
    reserve_allocation = {
        "Cash": cash_pct,
        "Bond": bond_pct,
        "Gold": gold_pct,
    }

    investment_allocation = {
        "Core": INVESTMENT_ALLOCATION["Core"] * investment_pct,
        "Growth": INVESTMENT_ALLOCATION["Growth"] * investment_pct,
        "Speculative": INVESTMENT_ALLOCATION["Speculative"] * investment_pct,
    }

    # --- Count number of assets for each type ---
    type_counts = {}
    for asset in assets:
        if asset.asset_type:
            type_counts[asset.asset_type] = type_counts.get(asset.asset_type, 0) + 1

    # --- Assign target percentage per asset ---
    for asset in assets:
        if asset.asset_type in reserve_allocation:
            count = type_counts.get(asset.asset_type, 0)
            if count > 0:
                asset.target = reserve_allocation[asset.asset_type] / count / 100
            else:
                asset.target = 0
        elif asset.asset_type in investment_allocation:
            count = type_counts.get(asset.asset_type, 0)
            if count > 0:
                asset.target = investment_allocation[asset.asset_type] / count / 100
            else:
                asset.target = 0
        else:
            asset.target = 0  # Unknown type fallback

    return assets
