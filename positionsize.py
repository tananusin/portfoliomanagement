# positionsize.py

def classify_position(weight_pct, target_pct, threshold=0.05): # Defaul threshold 5%
    # Calculate the drift
    drift = weight_pct - target_pct
    
    # Check if the position is oversized, undersized, or aligned
    if drift > threshold:
        return "oversize", drift
    elif drift < -threshold:
        return "undersize", drift
    else:
        return "-", drift
