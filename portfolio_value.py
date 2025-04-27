# portfolio_value.py
from fetch import get_price, get_fx_to_thb
from asset_data import AssetData
from typing import List

def enrich_asset(asset: AssetData) -> AssetData:
    # Handle THB currency first, set fx_rate to 1
    if asset.currency == 'THB':
        asset.fx_rate = 1
    else:
        # For other currencies, fetch fx_rate normally
        asset.fx_rate = get_fx_to_thb(asset.currency)

    # Handle BOND and CASH symbols separately for price and fx_rate
    if asset.symbol in ['BOND', 'CASH']:
        asset.price = 1
        # If currency is not THB, fetch fx_rate for BOND or CASH
        if asset.currency != 'THB':
            asset.fx_rate = get_fx_to_thb(asset.currency)
    else:
        # For other assets, fetch price normally
        asset.price = get_price(asset.symbol)
    
    # Calculate value if price and fx_rate are valid
    if asset.price is not None and asset.fx_rate is not None:
        asset.value_local = asset.shares * asset.price
        asset.value_thb = asset.value_local * asset.fx_rate
    
    return asset

def enrich_assets(assets: List[AssetData]) -> List[AssetData]:
    return [enrich_asset(asset) for asset in assets]

def calculate_portfolio_total(assets: List[AssetData]) -> float:
    return sum(asset.value_thb or 0 for asset in assets)

def assign_weights(assets: List[AssetData], total_value: float):
    for asset in assets:
        if asset.value_thb is not None:
            asset.weight = asset.value_thb / total_value