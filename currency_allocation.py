# currency_allocation.py

from typing import Iterable

from currency_portfolio import Currency, build_currency_objects


def build_currency_portfolio(
    assets: Iterable,
    investment_weight: float,
    bond_weight_total: float,
):
    """
    Build currency portfolio objects from asset-level target allocation.

    Assumed asset fields:
        asset.currency: str
        asset.target: float          # final portfolio target weight
        asset.assumed_mdd: float     # asset MDD as positive decimal, e.g. 0.20 for 20%

    Returns:
        currencies: list[Currency]
        currency_map: dict[str, Currency]

    Formulas:
        currency_investment_weight
            = sum(asset.target) for assets in that currency

        currency_investment_mdd
            = sum(asset.target * asset.assumed_mdd) for assets in that currency

        currency_cash_weight
            = currency_investment_mdd

        currency_cash_ratio
            = currency_cash_weight / total_cash_weight

        currency_bond_weight
            = bond_weight_total * currency_cash_ratio
    """

    # Collect currency names from valid assets
    currency_names = [
        asset.currency
        for asset in assets
        if getattr(asset, "currency", None)
    ]

    currencies, currency_map = build_currency_objects(currency_names)

    # Aggregate investment-side currency exposure
    for asset in assets:
        currency_name = getattr(asset, "currency", None)
        target = getattr(asset, "target", 0.0) or 0.0
        assumed_mdd = getattr(asset, "assumed_mdd", 0.0) or 0.0

        if not currency_name or target == 0:
            continue

        currency_name = currency_name.upper()
        ccy = currency_map[currency_name]

        ccy.currency_investment_weight += target
        ccy.currency_investment_mdd += target * assumed_mdd

    # Cash allocation by currency
    total_cash_weight = 0.0
    for ccy in currencies:
        ccy.currency_cash_weight = ccy.currency_investment_mdd
        total_cash_weight += ccy.currency_cash_weight

    # Cash ratio and bond allocation
    for ccy in currencies:
        if total_cash_weight > 0:
            ccy.currency_cash_ratio = ccy.currency_cash_weight / total_cash_weight
        else:
            ccy.currency_cash_ratio = 0.0

        ccy.currency_bond_weight = bond_weight_total * ccy.currency_cash_ratio

    return currencies, currency_map
