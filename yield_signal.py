# yield_signal.py
from typing import List
from asset_data import AssetData
from user_preferences import UserPreference

def assign_yield_signals(assets: List[AssetData], prefs: UserPreference) -> List[AssetData]:

    for asset in assets:
      if asset.asset_type is None:
            continue
      
        if asset.asset_type == "Speculative":
            dividend_yield_recovery = prefs.yield_speculative / 100
        elif asset.asset_type == "Growth":
            dividend_yield_recovery = prefs.yield_growth / 100
        elif asset.asset_type == "Core":
            dividend_yield_recovery = prefs.yield_core / 100
        else:
            asset.dividend_yield_signal = None
            continue
        
        asset.dividend_yield_recovery = dividend_yield_recovery
        
        if asset.dividend_yield > asset.dividend_yield_recovery:
            asset.dividend_yield_signal = "sufficient"
        else:
            asset.dividend_yield_signal = "-"

    return assets
