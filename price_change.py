# price_change.py
from typing import List
from asset_data import AssetData
from user_preferences import UserPreference

def assign_price_changes(assets: List[AssetData], prefs: UserPreference) -> List[AssetData]:
    """
    Classifies each asset as Overpriced, Underpriced, or Neutral based on price behavior vs user assumptions.
    """
    for asset in assets:
        if asset.asset_type is None:
            continue

        # Skip if required data is missing or zero (to avoid divide-by-zero)
        if (
            asset.price is None or asset.price == 0 or
            asset.high_52w is None or asset.high_52w == 0 or
            asset.low_52w is None or asset.low_52w == 0 or
            asset.low_3y is None or asset.low_3y == 0
        ):
            asset.price_change = None
            continue

        # --- Calculate Drop and Gain Rates ---
        asset.drop_1y = (asset.price - asset.high_52w) / asset.high_52w
        asset.gain_1y = (asset.price - asset.low_52w) / asset.low_52w
        asset.gain_3y = (asset.price - asset.low_3y) / asset.low_3y

        # --- Lookup user MDD and CAGR ---
        if asset.asset_type == "Speculative":
            mdd = prefs.mdd_speculative_pct / 100
            cagr = prefs.cagr_speculative_pct / 100
        elif asset.asset_type == "Growth":
            mdd = prefs.mdd_growth_pct / 100
            cagr = prefs.cagr_growth_pct / 100
        elif asset.asset_type == "Core":
            mdd = prefs.mdd_core_pct / 100
            cagr = prefs.cagr_core_pct / 100
        else:
            asset.price_change = None
            continue

        # --- Price Signal Logic ---
        # Priority: if both underpriced and overpriced conditions are true, classify as "underprice".
        if asset.drop_1y < mdd:  # dropped more than acceptable MDD
            asset.price_change = "oversold"
        elif asset.gain_1y > cagr or asset.gain_3y > (1 + cagr) ** 3 - 1:
            asset.price_change = "overbought"
        else:
            asset.price_change = "-"

    return assets

