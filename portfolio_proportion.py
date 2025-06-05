# portfolio_proportion.py
import streamlit as st
from asset_data import AssetData
from typing import List, Dict
from user_preferences import UserPreference

def count_asset_types(assets: List[AssetData]) -> Dict[str, int]:
    """
    Count how many assets exist in each type category.
    """
    type_list = ["Speculative", "Growth", "Core", "Gold", "Bond", "Cash"]
    count_dict = {t: 0 for t in type_list}

    for asset in assets:
        if asset.asset_type in count_dict:
            count_dict[asset.asset_type] += 1

    return count_dict

def calculate_investment_mdd(prefs: UserPreference) -> float:
    """
    Calculates the weighted maximum drawdown for the investment portion.
    """
    investment_pct = prefs.investment_pct

    mdd_investment = (
        prefs.mdd_core_pct * 0.6 +
        prefs.mdd_growth_pct * 0.3 +
        prefs.mdd_speculative_pct * 0.1
    ) * investment_pct / 100

    return abs(mdd_investment)  # Convert to positive %

def assign_targets(assets: List[AssetData], prefs: UserPreference) -> List[AssetData]:
    """
    Assigns target portfolio weights to each asset based on user preferences.
    """
    investment_pct = prefs.investment_pct
    reserve_pct = 100 - investment_pct

    # Calculate weighted MDD of investment portion
    mdd_investment = calculate_investment_mdd(prefs)

    # Calculate reserve allocation
    cash_pct = mdd_investment * investment_pct / 100
    gold_pct = 0.2 * reserve_pct    # Fixed: Gold is 20% of reserve
    bond_pct = reserve_pct - cash_pct - gold_pct

    if bond_pct < 0:
        st.error(
            f"⚠️ Not enough cash to cover maximum drawdown. "
            f"Consider lowering your investment portion below {investment_pct}%."
        )
        cash_pct += bond_pct  # reduce cash by overshoot
        bond_pct = 0.0        # prevent negative bond

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

    # --- Count assets per type ---
    type_counts = count_asset_types(assets)

    # --- Assign target percentage per asset ---
    for asset in assets:
        if asset.asset_type in reserve_allocation:
            count = type_counts.get(asset.asset_type, 0)
            asset.target = (reserve_allocation[asset.asset_type] / count / 100) if count > 0 else 0.0
        elif asset.asset_type in investment_allocation:
            count = type_counts.get(asset.asset_type, 0)
            asset.target = (investment_allocation[asset.asset_type] / count / 100) if count > 0 else 0.0
        else:
            asset.target = 0.0  # fallback for unknown asset_type

    return assets
