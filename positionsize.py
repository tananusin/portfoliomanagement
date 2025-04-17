# positionsize.py

import pandas as pd

def classify_position(weight_pct, target_pct, threshold=0.50): # Defaul %drift threshold 50%
    # Check if target is set
    if pd.isna(weight_pct) or pd.isna(target_pct) or target_pct == 0:
        return "unknown", 0
    
    # Calculate the drift    
    drift = (weight_pct - target_pct) / target_pct

    # Check if the position is oversized, undersized, or aligned
    if drift > threshold:
        return "oversize", drift
    elif drift < -threshold:
        return "undersize", drift
    else:
        return "-", drift
