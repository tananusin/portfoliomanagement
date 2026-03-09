# currency_portfolio.py

from dataclasses import dataclass

@dataclass
class Currency:
    name: str

    # Investment-side currency exposure
    currency_investment_weight: float = 0.0
    currency_investment_mdd: float = 0.0

    # Reserve-side allocation
    currency_cash_weight: float = 0.0
    currency_cash_ratio: float = 0.0
    currency_bond_weight: float = 0.0


def build_currency_objects(currency_names: list[str]):
    currency_names = sorted({n.upper() for n in currency_names})
    currencies = [Currency(name=n) for n in currency_names]
    currency_map = {c.name: c for c in currencies}
    return currencies, currency_map
