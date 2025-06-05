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

def calculate_investment_mdd(prefs: UserPreference, type_counts: Dict[str, int]) -> float:
    """
    Calculates the weighted maximum drawdown for the investment portion,
    dynamically adjusting weights based on available asset types.
    """
    investment_pct = prefs.investment_pct

    base_weights = {
        "Core": 0.6,
        "Growth": 0.3,
        "Speculative": 0.1,
    }

    # Only include types with non-zero count
    available_types = {k: v for k, v in base_weights.items() if type_counts.get(k, 0) > 0}

    if not available_types:
        return 0.0  # No investment assets

    total_weight = sum(available_types.values())

    adjusted_weights = {k: v / total_weight for k, v in available_types.items()}

    mdd_investment = sum([
        adjusted_weights.get("Core", 0.0) * prefs.mdd_core_pct,
        adjusted_weights.get("Growth", 0.0) * prefs.mdd_growth_pct,
        adjusted_weights.get("Speculative", 0.0) * prefs.mdd_speculative_pct,
    ]) * investment_pct / 100

    return abs(mdd_investment)

def assign_targets(assets: List[AssetData], prefs: UserPreference) -> List[AssetData]:
    investment_pct = prefs.investment_pct
    reserve_pct = 100 - investment_pct

    # --- Count assets per type ---
    type_counts = count_asset_types(assets)

    # --- Calculate weighted MDD of investment portion ---
    mdd_investment = calculate_investment_mdd(prefs, type_counts)

    # --- Reserve Allocation ---
    cash_pct = mdd_investment * investment_pct / 100

    gold_pct = 0.2 * reserve_pct if type_counts.get("Gold", 0) > 0 else 0.0
    bond_pct = reserve_pct - cash_pct - gold_pct

    if bond_pct < 0:
        st.error(
            f"⚠️ Not enough cash to cover portfolio maximum drawdown {cash_pct:.2f}%. "
            f"Consider lowering your investment portion below {investment_pct}%."
        )
        cash_pct += bond_pct
        bond_pct = 0.0

    if type_counts.get("Bond", 0) == 0:
        cash_pct += bond_pct
        bond_pct = 0.0

    reserve_allocation = {
        "Cash": cash_pct,
        "Bond": bond_pct,
        "Gold": gold_pct,
    }

    # --- Investment Allocation ---
    base_alloc = {"Core": 0.6, "Growth": 0.3, "Speculative": 0.1}
    available_types = {k: v for k, v in base_alloc.items() if type_counts.get(k, 0) > 0}

    if not available_types:
        st.error("❌ No investment assets found. Please add Core, Growth, or Speculative assets.")
        return assets

    total_weight = sum(available_types.values())
    investment_allocation = {
        k: (v / total_weight) * investment_pct
        for k, v in available_types.items()
    }

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

