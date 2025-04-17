# positionsize.py

def classify_position(weight_pct, target_pct, threshold=5.0):
    # Calculate the drift
    drift = weight_pct - target_pct
    
    # Check if the position is oversized, undersized, or aligned
    if drift > threshold:
        return "Oversized", drift
    elif drift < -threshold:
        return "Undersized", drift
    else:
        return "-", drift
