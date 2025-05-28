#pe_signal.py
from asset_data import AssetData
from typing import List

def assign_pe_signals(assets: List[AssetData]) -> None:
    for asset in assets:
        if asset.pe_ratio is None or asset.pe_p25 is None or asset.pe_p75 is None:
            asset.pe_signal = None
        elif asset.pe_ratio < asset.pe_p25:
            asset.pe_signal = "undervalued"
        elif asset.pe_ratio > asset.pe_p75:
            asset.pe_signal = "overvalued"
        else:
            asset.pe_signal = "-"
