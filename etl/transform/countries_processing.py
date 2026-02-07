import pandas as pd

def data_exploration(data: pd.DataFrame):
    print("\n\033[4m COUNTRIES PREPROCESSING BLOCK \033[0m")
    print("\n",data.columns)
    print("\n")
    data.info()
    print("\n",data.describe())
    print("\n",data.describe(include=['object']))
   
    print("\n\n\t😁😁😁😁End of data exploration😁😁👍😊\n\n")
    
def data_transformation(df: pd.DataFrame):
    #Drop column country code because it is unncessary for analysis
    if 'Countrycode' in df.columns:
        df.drop(columns="CountryCode", inplace=True)
    return df
def clean_data(df: pd.DataFrame):
    data_exploration(df)
    df=data_transformation(df)
    print("Data Cleaning complete for countries dataset!!\n")
    df.columns = [col.lower() for col in df.columns]    
    print(df.columns.tolist())
    return df


