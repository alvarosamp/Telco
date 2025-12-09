import pandas as pd

def _map_binary_series(s : pd.Series) -> pd.Series:
    """Map a binary series to 0 and 1.

    Args:
        s (pd.Series): Input binary series with values like 'yes'/'no', 'true'/'false', etc.

    Returns:
        pd.Series: Mapped series with values 0 and 1.
    """
    unique_values = s.dropna().unique()
    if len(unique_values) != 2:
        raise ValueError("Input series must be binary with exactly two unique values.")
    
    mapping = {unique_values[0]: 0, unique_values[1]: 1}
    return s.map(mapping)