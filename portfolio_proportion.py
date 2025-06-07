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
    return {t: sum(1 for a in assets if a.asset_type == t) for t in type_list}

def get_adjusted_weights(base_weights: Dict[str, float], type_counts: Dict[str, int]) -> Dict[str, float]:
    """
    Recalculate weights based only on available asset types.
    """
    available = {k: v for k, v in base_weights.items() if type_counts.get(k, 0) > 0}
    total = sum(available.values())
    return {k: v / total for k, v in available.items()} if total > 0 else {}

def calculate_investment_mdd(prefs: UserPreference, type_counts: Dict[str, int]) -> float:
    """
    Calculates the weighted MDD for the investment portion.
    """
    base_weights = {"Core": 0.6, "Growth": 0.3, "Speculative": 0.1}
    weights = get_adjusted_weights(base_weights, type_counts)
    mdd = sum([
        weights.get("Core", 0.0) * prefs.mdd_core_pct,
        weights.get("Growth", 0.0) * prefs.mdd_growth_pct,
        weights.get("Speculative", 0.0) * prefs.mdd_speculative_pct,
    ])
    return abs(mdd) * prefs.investment_pct / 100

def assign_proportional_allocation(
    assets: List[AssetData],
    allocations: Dict[str, float],
    type_counts: Dict[str, int],
    eligible_types: List[str]
) -> None:
    """
    Assign target percentage to eligible asset types based on allocation and count.
    """
    for asset in assets:
        a_type = asset.asset_type
        if a_type in allocations and a_type in eligible_types:
            count = type_counts.get(a_type, 0)
            asset.target = (allocations[a_type] / count / 100) if count > 0 else 0.0

def assign_targets(assets: List[AssetData], prefs: UserPreference) -> List[AssetData]:
    type_counts = count_asset_types(assets)
    investment_pct = prefs.investment_pct
    gold_pct = prefs.gold_pct
    reserve_pct = 100 - investment_pct

    # --- Investment Allocation ---
    investment_weights = get_adjusted_weights({"Core": 0.6, "Growth": 0.3, "Speculative": 0.1}, type_counts)
    if not investment_weights:
        st.error("❌ No investment assets found. Please add Core, Growth, or Speculative assets.")
        return assets

    investment_allocation = {k: v * investment_pct for k, v in investment_weights.items()}

    # --- Reserve Allocation ---
    mdd_investment = calculate_investment_mdd(prefs, type_counts)
    cash_pct = mdd_investment * investment_pct / 100
    gold_pct = gold_pct/100 * reserve_pct if type_counts.get("Gold", 0) > 0 else 0.0
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

    # --- Assign Targets ---
    assign_proportional_allocation(assets, reserve_allocation, type_counts, eligible_types=["Cash", "Bond", "Gold"])
    assign_proportional_allocation(assets, investment_allocation, type_counts, eligible_types=list(investment_allocation.keys()))

    return assets

