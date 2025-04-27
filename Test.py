from dataclasses import dataclass

@dataclass
class StockData:
    # Google Sheet Variables
    name: str
    ticker: str
    currency: str
    shares: float
    target: float
    asset_type: str

    # Portfolio Variables
    price: float
    fx: float
    value_local: float
    value_thb: float
    weight: float