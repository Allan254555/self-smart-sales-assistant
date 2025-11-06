import pandas as pd


def data_exploration(data: pd.DataFrame):
    print("\n\033[4m CUSTOMER PREPROCESSING BLOCK \033[0m")
    print("\n",data.columns)
    print("\n")
    data.info()
    print("\n",data.describe())
    print("\n",data.describe(include=['object']))
    print("\n",data.head())
    print("\n\n\t😁😁😁😁End of data exploration😁😁👍😊\n\n")
    
def missing_values(data: pd.DataFrame):
    missing_values = data.isnull().sum().sum()
    if missing_values:
        print(f"Total missing values: {missing_values}")
        print("Total missing values per column:\n",data.isnull().sum())
    else:
        print("No missing values found!!!")
    return data
def clean_data(df: pd.DataFrame):
    data_exploration(df)
    df = missing_values(df) 
    df.columns = [col.lower() for col in df.columns]    
    print(df.head())
    return df