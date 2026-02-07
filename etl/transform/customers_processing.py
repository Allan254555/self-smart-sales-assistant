import pandas as pd
'''from etl.extract.load_data import load_customers
data = load_customers()'''

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
def data_transformation(data: pd.DataFrame):
    #Join first name and last name to full name
    
    data["customername"]=data["FirstName"] + " " + data["LastName"].str.strip()

    #Drop middle initial
    if "MiddleInitial" in data.columns:
        data.drop(columns=["MiddleInitial"], inplace=True)
    
    #Drop name columns
    data.drop(columns=["FirstName", "LastName", "Address"], inplace=True)
    print(data.columns.tolist())
    return data

def clean_data(df: pd.DataFrame):
    #data_exloration(df)
    df=data_transformation(df)
    df = missing_values(df) 
    df.columns = [col.lower() for col in df.columns]    
    print(df.columns.tolist())
    return df