# currency_allocation.py

from typing import Iterable

from asset_data import AssetData
from currency_portfolio import build_currency_objects


def build_currency_portfolio(
    assets: Iterable[AssetData],
    bond_weight_total: float,
):
    """
    Build currency portfolio from asset-level target allocation.

    Required asset fields:
        asset.currency
        asset.target
        asset.mdd

    Returns:
        currencies: list[Currency]
        currency_map: dict[str, Currency]

    Formulas:
        currency_investment_weight
            = Σ(asset.target)

        currency_investment_mdd
            = Σ(asset.target * asset.mdd)

        currency_cash_weight
            = currency_investment_mdd

        currency_cash_ratio
            = currency_cash_weight / total_cash_weight

        currency_bond_weight
            = bond_weight_total * currency_cash_ratio
    """

    # Build currency objects from asset currencies
    currency_names = [
        asset.currency
        for asset in assets
        if asset.currency
    ]
    currencies, currency_map = build_currency_objects(currency_names)

    # Aggregate by currency
    for asset in assets:
        if not asset.currency:
            continue

        currency_name = asset.currency.upper()
        target = asset.target or 0.0
        mdd = asset.mdd or 0.0

        ccy = currency_map[currency_name]
        ccy.currency_investment_weight += target
        ccy.currency_investment_mdd += target * mdd

    # Currency cash weight
    total_cash_weight = 0.0
    for ccy in currencies:
        ccy.currency_cash_weight = ccy.currency_investment_mdd
        total_cash_weight += ccy.currency_cash_weight

    # Currency cash ratio and bond weight
    for ccy in currencies:
        if total_cash_weight > 0:
            ccy.currency_cash_ratio = ccy.currency_cash_weight / total_cash_weight
        else:
            ccy.currency_cash_ratio = 0.0

        ccy.currency_bond_weight = bond_weight_total * ccy.currency_cash_ratio

    return currencies, currency_map
