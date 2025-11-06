import pandas as pd
import numpy as np

def data_exploration(df: pd.DataFrame):
    print("\n\033[4m CATEGORIES PREPROCESSING BLOCK \033[0m")
    print("\n",df.columns)
    print("\n")
    print("\n",df.info())
    print("\n",df.describe())
    print("\n",df.describe(include=['object']))
    print("\n",df["CategoryName"].unique())
    print("\n",df)
    print("\n\tEnd of data exploration!!!\n")
def dealing_with_null_values(df: pd.DataFrame): 
    
    total_missing = df.isnull().sum().sum()
    if total_missing == 0:
        print("No missing Values found!")
    else:
        print(f"Total missing values: {total_missing}\n")
        print("\n")
    return df

def duplicate_handling(df: pd.DataFrame):
    #detect duplicates
    duplicates=df[df.duplicated(subset=["CategoryName"])]
    if len(duplicates) > 0:
        print("Here are duplicates: \n",duplicates)
    else:
        print("No duplicates found!!!")
    return df
def clean_data(df: pd.DataFrame):
    data_exploration(df)
    df=dealing_with_null_values(df)
    df=duplicate_handling(df)
    df.columns = [col.lower() for col in df.columns]    
    print(df.head())
    print("\nEnd of Categories data pre processing\n\n")
    return df


