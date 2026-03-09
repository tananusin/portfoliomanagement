# portfolio_value.py
from typing import List
from asset_data import AssetData

def calculate_asset_value(asset: AssetData) -> None:
    """
    Compute value_local and value_thb for an asset if price and fx_rate are available.
    """
    if asset.price is not None and asset.fx_rate is not None:
        asset.value_local = asset.shares * asset.price
        asset.value_thb = asset.value_local * asset.fx_rate

def summarize_assets(assets: List[AssetData]) -> List[AssetData]:
    # Ensure all value fields are populated
    for asset in assets:
        calculate_asset_value(asset)
    return assets


def calculate_portfolio_total(assets: List[AssetData]) -> float:
    return sum(asset.value_thb or 0 for asset in assets)


def assign_weights(assets: List[AssetData], total_value: float) -> float:
    """
    Assign actual portfolio weights and return estimated portfolio MDD
    as the weighted sum of asset assumed_mdd.
    """
    portfolio_estimated_mdd = 0.0

    for asset in assets:
        if asset.value_thb is not None and total_value > 0:
            asset.weight = asset.value_thb / total_value
        else:
            asset.weight = 0.0

        if asset.weight is not None and asset.assumed_mdd is not None:
            portfolio_estimated_mdd += asset.weight * asset.assumed_mdd

    return portfolio_estimated_mdd

def combine_assets(assets: List[AssetData]) -> List[AssetData]:
    """
    Combine bonds and cash into summary positions.
    Preserve both actual value and target allocation.
    """
    for asset in assets:
        calculate_asset_value(asset)

    bond_assets = [a for a in assets if a.asset_class == "Bond"]
    cash_assets = [a for a in assets if a.asset_class == "Cash"]
    other_assets = [a for a in assets if a.asset_class not in {"Cash", "Bond"}]

    def _summarize_group(assets_to_sum, name, asset_class):
        total_value_thb = sum(a.value_thb or 0 for a in assets_to_sum)
        total_target = sum(a.target or 0 for a in assets_to_sum)

        if total_value_thb == 0 and total_target == 0:
            return None

        return AssetData(
            name=name,
            symbol=name.upper().replace(" ", "_"),
            currency="THB",
            shares=1,
            price=1,
            asset_class=asset_class,
            fx_rate=1,
            value_local=total_value_thb,
            value_thb=total_value_thb,
            target=total_target,
        )

    summarized = []

    total_bond = _summarize_group(bond_assets, "Total Bond", "Bond")
    total_cash = _summarize_group(cash_assets, "Total Cash", "Cash")

    if total_bond:
        summarized.append(total_bond)
    if total_cash:
        summarized.append(total_cash)

    return other_assets + summarized
