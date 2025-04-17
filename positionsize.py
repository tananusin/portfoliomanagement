# positionsize.py

import pandas as pd

def classify_position(weight_pct, target_pct, threshold=1.0):
    """
    Compare actual weight vs. target weight.

    Returns a tuple:
    - status: 'undersize', 'oversize', 'aligned', or 'unknown'
    - drift: actual weight % - target %
    """
    if pd.isna(weight_pct) or pd.isna(target_pct):
        return "unknown", None

    drift = weight_pct - target_pct

    if abs(drift) <= threshold:
        return "aligned", drift
    elif drift > threshold:
        return "oversize", drift
    else:
        return "undersize", drift
