import pandas as pd 

def preprocess_data(df: pd.DataFrame, target_col: str = 'None') -> pd.DataFrame:
    """
    Basic cleaning for Telco churn 
    - trim column names
    - drop obvious ID cols
    - Fix total charges to numeric
    - Map target column to 0/1 if specified
    - Simple NA handling
    """"

    #Tidy headers 
    df.columns = df.columns.str.strip()#Remove leading/trailing spaces

    #Drop ID columns
    id_cols = ['customerID', 'customer_id', 'CustomerId']
    for col in id_cols:
        if col in df.columns:
            df = df.drop(columns=[col])

    