# asset_data.py
from dataclasses import dataclass
from typing import Optional  # If User Leave Input Empty

@dataclass
class AssetData:
    name: str
    symbol: str
    currency: str
    shares: float
    target: Optional[float] = None
    asset_type: Optional[str] = None

    price: Optional[float] = None
    fx_rate: Optional[float] = None
    value_local: Optional[float] = None
    value_thb: Optional[float] = None
    portfolio_total_thb: Optional[float] = None
    weight: Optional[float] = None
