import pandas as pd

pd.set_option("display.max_columns", None)
def products_data_exploration(products: pd.DataFrame):
    print("\n\033[4m PRODUCTS PREPROCESSING BLOCK \033[0m")
    print("\n",products.columns)
    print("\n")
    print("\n",products.info())
    print("\n",products.describe(include=['object']))
    print("\n",products.head())
    print("\n\n\t😁😁😁😁End of data exploration😁😁👍😊\n\n")


def dealing_with_null_values(products: pd.DataFrame): 
    #Checking null values 
    
    total_missing = products.isnull().sum().sum()
    if total_missing == 0:
        print("No missing Values found!")
    else:
        print(f"Total missing values: {total_missing}\n")
        print("Total missing values per column:\n",products.isnull().sum())

        print("\n")
    return products


def duplicate_handling_feature_handling(products):
    #detect duplicates
    df=products
    duplicates=df[df.duplicated(subset=["ProductName"])]
    if not duplicates.empty:
        print("Here are duplicates: \n",duplicates)
    else:
        print("No duplicates Found.")
    return df


def data_transformation(data):
  
    #Drop unnecessary name columns
    data.drop(columns=["ModifyDate", "Resistant"], inplace=True)
    data["VitalityDays"].describe()
    data["VitalityDays"] = data["VitalityDays"].round().astype(int)

    print(data.columns)
    return data
    
def clean_data(df: pd.DataFrame):
    products_data_exploration(df)
    data = dealing_with_null_values(df)
    df_0 = duplicate_handling_feature_handling(data)
    df = data_transformation(df_0)
    df.columns = [col.lower() for col in df.columns]    
    print(df.columns.tolist())
    return df
