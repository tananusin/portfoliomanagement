# price_signal.py
from typing import List
from asset_data import AssetData
from user_preferences import UserPreference

def assign_price_signals(assets: List[AssetData], prefs: UserPreference) -> List[AssetData]:
    """
    Classifies each asset as Overpriced, Underpriced, or Neutral based on price behavior vs user assumptions.
    """
    for asset in assets:
        if asset.asset_type is None:
            continue

    # Skip if required data is missing or zero (to avoid divide-by-zero)
    if (
        asset.price is None or asset.price == 0 or
        asset.peak_1y is None or asset.peak_1y == 0 or
        asset.trough_1y is None or asset.trough_1y == 0 or
        asset.trough_3y is None or asset.trough_3y == 0
    ):
        asset.price_signal = None
        continue

        # --- Calculate Drop and Gain Rates ---
        asset.drop_1y = (asset.price - asset.peak_1y) / asset.peak_1y
        asset.gain_1y = (asset.price - asset.trough_1y) / asset.trough_1y
        asset.gain_3y = (asset.price - asset.trough_3y) / asset.trough_3y

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
            asset.price_signal = None
            continue

        # --- Price Signal Logic ---
        if asset.drop_1y < mdd:  # dropped more than acceptable MDD
            asset.price_signal = "underprice"
        elif asset.gain_1y > cagr or asset.gain_3y > (1 + cagr) ** 3 - 1:
            asset.price_signal = "overprice"
        else:
            asset.price_signal = "-"

    return assets
