import pandas as pd 
import os 

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The loaded data as a pandas DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
    
    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        raise IOError(f"An error occurred while reading the file: {e}")
    
    return data