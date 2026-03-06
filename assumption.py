# assumption.py

from asset_data import AssetData
from user_preferences import UserPreference


def calculate_assumption(asset: AssetData, user_pref: UserPreference) -> None:
    """Calculate assumption metrics for a single asset"""

    # Rebound
    if asset.mdd is not None:
        asset.rebound = 1 / (1 + asset.mdd) - 1    #asset.mdd is negative

    # CAGR
    if asset.rebound is not None:
        years = user_pref.years_rebound
        asset.cagr = (1 + asset.rebound) ** (1 / years) - 1

    # Dividend Yield Offset
    if asset.rebound is not None and asset.dividend_yield:
        asset.dividend_yield_offset = asset.rebound/asset.dividend_yield
        

def calculate_assumptions(assets: list[AssetData], user_pref: UserPreference) -> None:
    """
    Calculate assumptions for the entire portfolio
    """
    for asset in assets:
        calculate_assumption(asset, user_pref)
