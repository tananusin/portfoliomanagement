#pe_signal.py
from asset_data import AssetData
from typing import List

def assign_pe_signals(assets: List[AssetData]) -> None:
    for asset in assets:
        if (
            asset.pe_ratio is None or asset.pe_ratio == 0 or
            asset.pe_p25 is None or asset.pe_p25 == 0 or
            asset.pe_p75 is None or asset.pe_p75 == 0
        ):
            asset.pe_signal = "-"
        elif asset.pe_ratio < asset.pe_p25:
            asset.pe_signal = "undervalue"
        elif asset.pe_ratio > asset.pe_p75:
            asset.pe_signal = "overvalue"
        else:
            asset.pe_signal = "-"
