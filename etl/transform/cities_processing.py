import pandas as pd

def data_exploration(data: pd.DataFrame):
    print("\n\033[4m CITIES PREPROCESSING BLOCK \033[0m")
    print("\n",data.columns)
    print("\n")
    data.info()
    print("\n",data.describe())
    print("\n",data.describe(include=['object']))
    print("\n",data.head())
    
    #Check for missing values
    
    if data.isnull().sum().sum() == 0:
        print("\nNo missing values found!!!")
    else:
        print("Total missing values: ",data.isnull().sum().sum())
        print("Total missing values per column:\n", data.isnull().sum())
    #Check for duplicates
    duplicates=data[data.duplicated(subset=["CityName"])]
    if len(duplicates) > 0:
        print("Here are duplicates: \n",duplicates)
    else:
        print("No duplicates found!!!")
    
    return data
def data_transformation(df: pd.DataFrame):
    #Drop column country code because it is unncessary for analysis
    if 'Zipcode' in df.columns:
        df.drop(columns=["Zipcode"], inplace=True)
    return df
def clean_data(df: pd.DataFrame):
    df_0 = data_exploration(df)
    df = data_transformation(df_0)
    print("\n\n\t😁😁😁😁End of cities data pre processing😁😁👍😊\n\n")
    df.columns = [col.lower() for col in df.columns] 
    print(df.head())
    return df
