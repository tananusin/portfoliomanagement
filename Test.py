from dataclasses import dataclass

@dataclass
class StockData:
    # Google Sheet Variables
    name: str
    ticker: str
    asset_type: str
    currency: str
    shares: float
    target: Optional[float]	#If User Leave Google Sheet Cell Empty

    # Portfolio Variables
    price: float
    fx: float
    value_local: float
    value_thb: float
    weight: float