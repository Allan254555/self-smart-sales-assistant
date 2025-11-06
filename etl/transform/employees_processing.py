import pandas as pd

def data_exploration(data: pd.DataFrame):
    
    print("\n\033[4m EMPLOYEE PREPROCESSING BLOCK \033[0m")
    print("\n",data.columns)
    print("\n")
    data.info()
    print("\n",data.describe())
    print("\n",data.describe(include=['object']))
    print("\n",data.head())
    print("\n\n\t😁😁😁😁End of data exploration😁😁👍😊\n\n")
    
    missing_values = data.isnull().sum().sum()
    if missing_values:
        print(f"Total missing values: {missing_values}")
        print("Total missing values per column:\n",data.isnull().sum())
    else:
        print("No missing values found!!!")
    
    duplicates=data[data.duplicated(subset=["EmployeeID"])]
    if len(duplicates) > 0:
        print("Here are duplicates: \n",duplicates)
    else:
        print("No duplicates found!!!")
    return data

def clean_data(df: pd.DataFrame):
    df=data_exploration(df)
    df.columns = [col.lower() for col in df.columns]    
    print(df.head())
    return df