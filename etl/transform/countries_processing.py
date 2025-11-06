import pandas as pd

def data_exploration(data: pd.DataFrame):
    print("\n\033[4m COUNTRIES PREPROCESSING BLOCK \033[0m")
    print("\n",data.columns)
    print("\n")
    data.info()
    print("\n",data.describe())
    print("\n",data.describe(include=['object']))
   
    print("\n\n\t😁😁😁😁End of data exploration😁😁👍😊\n\n")
    
def dealing_with_null_values(data: pd.DataFrame):
    print("Total missing values per column:\n",data.isnull().sum())
    print("Total missing values: ",data.isnull().sum().sum())
    missing_rows = data[data.isnull().any(axis=1)]
    if missing_rows.empty:
        print("No rows with missing values.")
    else:
        print("Rows with missing values:")
        print(missing_rows)
    
    data["CountryCode"]= data["CountryCode"].fillna("AUS")

    print(data.sort_values(by="CountryCode"))
    return data
def clean_data(df: pd.DataFrame):
    data_exploration(df)
    df=dealing_with_null_values(df)
    print("Data Cleaning complete for countries dataset!!\n")
    df.columns = [col.lower() for col in df.columns]    
    print(df.head())
    return df


