# positionsize.py

import pandas as pd

def classify_position(weight_pct, target_pct, drift_threshold=0.05, drift_pct_threshold=0.50):
    # Check if target is set
    if pd.isna(weight_pct) or pd.isna(target_pct) or target_pct == 0:
        drift = 0
        return "-"
    
    # Calculate raw drift and percentage drift
    drift = weight_pct - target_pct
    drift_pct = drift / target_pct

    # Check if the position is oversized, undersized, or aligned
    if drift > drift_threshold or drift_pct > drift_pct_threshold:
        return "oversize"
    elif drift < -drift_threshold or drift_pct < drift_pct_threshold:
        return "undersize"
    else:
        return "-"
