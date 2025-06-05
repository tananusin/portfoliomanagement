#counting_asset_type.py
from typing import List, Dict
from asset_data import AssetData

def count_asset_types(assets: List[AssetData]) -> Dict[str, int]:
    type_list = ["Speculative", "Growth", "Core", "Gold", "Bond", "Cash"]
    count_dict = {t: 0 for t in type_list}

    for asset in assets:
        if asset.asset_type in count_dict:
            count_dict[asset.asset_type] += 1

    return count_dict
