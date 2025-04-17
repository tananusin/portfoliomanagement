# positionsize.py

def classify_position(weight_pct, target_pct, threshold=0.2):
    """
    Compares actual weight to target and returns drift status.
    
    Parameters:
    - weight_pct: Actual portfolio weight (float)
    - target_pct: Target portfolio weight (float)
    - threshold: Allowed drift percentage (default 20%)

    Returns:
    - "undersized", "oversized", or "on target"
    """
    if pd.isna(weight_pct) or pd.isna(target_pct):
        return "n/a"
    
    lower_bound = target_pct * (1 - threshold)
    upper_bound = target_pct * (1 + threshold)

    if weight_pct < lower_bound:
        return "undersized"
    elif weight_pct > upper_bound:
        return "oversized"
    else:
        return "on target"