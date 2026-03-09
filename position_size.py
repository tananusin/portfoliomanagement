# position_size.py
from asset_data import AssetData
from user_preferences import UserPreference
from typing import List


def set_position_size(asset: AssetData, user_pref: UserPreference) -> None:
    """
    Calculate drift, drift_relative and classify position size.
    """

    drift_threshold = user_pref.threshold_drift
    drift_relative_threshold = user_pref.threshold_drift_relative

    # Skip if weight or target missing
    if asset.weight is None or asset.target is None:
        asset.drift = None
        asset.drift_relative = None
        asset.position_size = "-"
        return

    # Target = 0 → treat entire weight as excess
    if asset.target == 0:
        asset.drift = asset.weight
        asset.drift_relative = None
        asset.position_size = "oversize"
        return

    # Calculate drift
    asset.drift = asset.weight - asset.target
    asset.drift_relative = asset.drift / asset.target

    # Position classification
    if asset.drift < -drift_threshold or asset.drift_relative < -drift_relative_threshold:
        asset.position_size = "undersize"

    elif asset.drift > drift_threshold or asset.drift_relative > drift_relative_threshold:
        asset.position_size = "oversize"

    else:
        asset.position_size = "-"


def assign_position_sizes(
    assets: List[AssetData],
    user_pref: UserPreference
) -> List[AssetData]:
    """
    Apply position size classification to all assets.
    """

    for asset in assets:
        set_position_size(asset, user_pref)

    return assets
