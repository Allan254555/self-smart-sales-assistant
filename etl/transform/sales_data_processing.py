import pandas as pd
import numpy as np


def sales_exloration(sales,products):
    print("\n\033[4m SALES PREPROCESSING BLOCK \033[0m")
    print(sales.head())
    print(sales.columns)
    sales.info()
    print(sales.describe())
    print(sales.describe(include=['object']))
    print(products.head())
    print("\nEnd of data exploration")
    print("\n`````````````````````````````````````````\n")
    
def dealing_with_missing_data(sales):
    """
        Replace missing values with random values date data
    """
    print("\n\033[1;4;33mMISSING DATA HANDLING BLOCK\033[0m\n")
    #Show missing values
    missing_values = sales.columns[sales.isnull().any()]
    if missing_values.empty:
        print("No missing values!")
    
    else:
        print("Columns with missing Values ",missing_values.to_list())
        print(f"Total missing values in columns {missing_values.to_list()}: ",sales[missing_values].isnull().sum().sum())
        print("Total missing values: ",sales.isnull().sum().sum())
        
    #Convert the SalesDate values to datetime from object dtype
    sales["SalesDate"] = pd.to_datetime(sales["SalesDate"], errors="coerce")
    date_col = "SalesDate"

    #Define random date rande
    start = pd.to_datetime("2018-01-01 00:00:00.000")
    end = pd.to_datetime("2018-05-31 23:59:59.999")

    start_sec = int(start.timestamp())
    end_sec = int(end.timestamp())
    
    #Missing SalesDate values
    n_missing = sales[date_col].isnull().sum()
    if n_missing > 0:
        print(f"Missing values before filling: {n_missing}")
        
        random_seconds = np.random.randint(start_sec, end_sec, size=n_missing)
        random_dates = pd.to_datetime(random_seconds, unit="s")

        # add random milliseconds
        random_ms = np.random.randint(0, 1000, size=n_missing)
        random_dates = random_dates + pd.to_timedelta(random_ms, unit="ms")
        #Fill missing values
        sales.loc[sales[date_col].isnull(), date_col] = random_dates
    
    #convert back into a string
    sales[date_col] = sales[date_col].dt.strftime("%Y-%m-%d %H:%M:%S.%f").str[:-3]
    
    #Check again after filling
    n_missing_after = sales[date_col].isnull().sum()
    print(f"Missing values after filling: {n_missing_after}")
    
    print("\nEnd of handling missing values") 
    
    return sales
def dublicate_handling(df):
    print("\n\033[1;4;35mDUPLICATE DATA HANDLING BLOCK\033[0m\n")
    duplicated_sales = df["TransactionNumber"].value_counts()
    duplicates_only = duplicated_sales[duplicated_sales > 1]
    
    print("number of repeated sales: ",len(duplicates_only))
    
    #Duplicate rows
    dup_rows = df.duplicated().sum()
    print(f"Found {dup_rows} duplicate rows")
    
    return df

def feature_scaling(sales, products):
    print("\n\033[5;1;4;31mFEATURE SCALING BLOCK\033[0m\n")
    
    #Validate columns in the datasets
    requires_columns = ["ProductID", "Quantity", "Discount"]
    for col in requires_columns:
        if col not in sales.columns:
            raise KeyError(f"Missing required columns: {col}")
    
    #Compute total price and merge
    df = sales.merge(products[["ProductID", "Price"]], on="ProductID", how="left")
    df["TotalPrice"] = df["Quantity"] * df["Price"] * (1-df["Discount"].fillna(0))
    
    print(df.sort_values(by="ProductID").head())
    df.info()
    print(df.head())
    print("Total missinng values: ",df.isnull().sum().sum())
    
    df = df.drop(columns=["Price"])
  
    print("\nEnd of feature scaling:\n\n")
    print("\n`````````````````````````````````````````")
    return df

def clean_data(sales,products):
    sales_exloration(sales,products)
    sales = dealing_with_missing_data(sales)
    dublicate_handling(sales)
    data=feature_scaling(sales,products)
    data.columns = [col.lower() for col in data.columns]    
    print(data.head())
    return data


