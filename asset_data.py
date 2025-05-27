# asset_data.py
from dataclasses import dataclass
from typing import Optional  # If User Leave Input Empty

@dataclass
class AssetData:
    # Google Sheet Variables
    name: str
    symbol: str
    currency: str
    shares: float
    price: Optional[float] = None
    fx_rate: Optional[float] = None
    asset_type: Optional[str] = None

    # Portfolio Value Variables
    value_local: Optional[float] = None
    value_thb: Optional[float] = None
    weight: Optional[float] = None

    # Proportion
    target: Optional[float] = None

    # Position Size
    drift: Optional[float] = None
    drift_pct: Optional[float] = None
    position_size: Optional[str] = None

    # Price Signal
    peak_1y: Optional[float] = None
    trough_1y: Optional[float] = None
    trough_3y: Optional[float] = None
    drop_1y: Optional[float] = None
    gain_1y: Optional[float] = None
    gain_3y: Optional[float] = None
    price_signal: Optional[str] = None

    # Fundamental Ratios
    pe_ratio: Optional[float] = None           # Trailing P/E ratio
    pe_mean: Optional[float] = None
    pe_sd: Optional[float] = None
    dividend_yield: Optional[float] = None      # Trailing dividend yield
