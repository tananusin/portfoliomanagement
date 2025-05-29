# yield_signal.py
from typing import List
from asset_data import AssetData
from user_preferences import UserPreference
import streamlit as st

def print_ABC():
    st.write("ABC")
 
def assign_yield_signals(assets: List[AssetData], prefs: UserPreference) -> List[AssetData]:

    for asset in assets:
      if asset.asset_type is None:
            continue
      
        if asset.asset_type == "Speculative":
            asset.dividend_yield_recovery = prefs.yield_speculative / 100
        elif asset.asset_type == "Growth":
            asset.dividend_yield_recovery = prefs.yield_growth / 100
        elif asset.asset_type == "Core":
            asset.dividend_yield_recovery = prefs.yield_core / 100
        else:
            asset.dividend_yield_signal = None
            continue
        
        if asset.dividend_yield is not None and asset.dividend_yield >= asset.dividend_yield_recovery:
            asset.dividend_yield_signal = "sufficient"
        else:
            asset.dividend_yield_signal = "insufficient"

    return assets
