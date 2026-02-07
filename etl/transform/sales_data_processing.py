import pandas as pd
import numpy as np    

pd.set_option("display.max_columns", None)

def sales_exloration(sales,products):
    #print("\n\033[4m SALES PREPROCESSING BLOCK \033[0m")
    #print(sales.head())
    #print(sales.columns)
    sales.info()
    #print(sales.describe())
    #print(sales.describe(include=['object']))
    #print(products.head())
    #print("\nEnd of data exploration")
    #print("\n`````````````````````````````````````````\n")
    missing_values = sales.columns[sales.isnull().any()]
    #print("Columns with missing Values ",missing_values.to_list())          
    #print(f"Total missing values in columns {missing_values.to_list()}: ",sales[missing_values].isnull().sum().sum())


#sales_exloration(sales,products)
    
    
def dealing_with_missing_data(sales):
    """
        Drop missing Data
        Why this is the best choice:

            Only ~1% of data → negligible loss

            Time-based sampling requires valid dates

            Imputation would introduce fake trends

            Keeps data honest and explainable
    """
    #print("\n\033[1;4;33mMISSING DATA HANDLING BLOCK\033[0m\n")
    #Show missing values
    missing_values = sales.columns[sales.isnull().any()]
    if missing_values.empty:
        print("No missing values!")
    
    else:
        print("Columns with missing Values ",missing_values.to_list())
        #print(f"Total missing values in columns {missing_values.to_list()}: ",sales[missing_values].isnull().sum().sum())
        #print("Total missing values: ",sales.isnull().sum().sum())
    
    date_col = "SalesDate"    
    #Convert the SalesDate values to datetime from object dtype
    sales[date_col] = pd.to_datetime(sales[date_col], errors="coerce")
    
    #print(len(sales))
    
    #Missing SalesDate values
    n_missing = sales[date_col].isnull().sum()
    if n_missing > 0:
        #print(f"Missing values before dropping: {n_missing}")
        sales = sales.dropna(subset=[date_col])
    else:
        print("No missing values!")
    #Check again after dropping
    n_missing_after = sales[date_col].isnull().sum()
    #print(f"Missing values after dropping: {n_missing_after}")
    #print(len(sales))
    #print("\nEnd of handling missing values") 
    
    return sales


def dublicate_handling(df):
    #print("\n\033[1;4;35mDUPLICATE DATA HANDLING BLOCK\033[0m\n")
    duplicated_sales = df["TransactionNumber"].value_counts()
    duplicates_only = duplicated_sales[duplicated_sales > 1]
    
    #print("number of repeated sales: ",len(duplicates_only))
    
    #Duplicate rows
    dup_rows = df.duplicated().sum()
    #print(f"Found {dup_rows} duplicate rows")
    
    return df

def feature_scaling(sales, products):
    print("\n\033[5;1;4;31mFEATURE SCALING BLOCK\033[0m\n")
    
     # normalize column names (strip spaces + lowercase)
    sales.columns = sales.columns.str.strip().str.lower()
    products.columns = products.columns.str.strip().str.lower()

    #Validate columns in the datasets
    requires_columns = ["productid", "quantity", "discount"]
    for col in requires_columns:
        if col not in sales.columns:
            raise KeyError(f"Missing required columns: {col}. Available: {sales.columns.tolist()}")
    
    #Compute total price and merge
    df = sales.merge(products[["productid", "price"]], on="productid", how="left")
    df["totalprice"] = df["quantity"] * df["price"] * (1-df["discount"].fillna(0))
    
    #print(df.sort_values(by="ProductID").head())
    df.info()
    #print(df.head())
    #print("Total missinng values: ",df.isnull().sum().sum())
    
    df = df.drop(columns=["price"])
  
    #print("\nEnd of feature scaling:\n\n")
    #print("\n`````````````````````````````````````````")
    return df

def clean_data(sales,products):
    sales_exloration(sales,products)
    sales = dealing_with_missing_data(sales)
    dublicate_handling(sales)
    data=feature_scaling(sales,products)
    data.columns = [col.lower() for col in data.columns] 
    print(data.head())
    print(data.columns.tolist(), len(data))   
    return data


