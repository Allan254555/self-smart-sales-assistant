from etl.load import database_loader
from etl.extract import load_data
from etl.transform import (
    categories_processing,
    cities_processing,
    countries_processing,
    customers_processing,
    employees_processing,
    products_processing,
    sales_data_processing
)
#from etl.load import database_loader

import pandas as pd

import pandas as pd
import numpy as np


def main():
    print("=== Starting ETL Pipeline ===")

    print("Extracting data...")
    '''categories = load_data.load_categories()
    cities = load_data.load_cities()
    countries = load_data.load_countries()    
    customers = load_data.load_customers()
    employees = load_data.load_employees()'''
    products = load_data.load_products()
    sales = load_data.load_sales()
    
   
  
    print("Transforming data...")
    '''categories_df = categories_processing.clean_data(categories)
    cities_df = cities_processing.clean_data(cities)
    countries_df = countries_processing.clean_data(countries)
    customers_df = customers_processing.clean_data(customers)
    employees_df = employees_processing.clean_data(employees)
    products_df = products_processing.clean_data(products)'''
    sales_df = sales_data_processing.clean_data(sales,products)


    print("Loading data into the database...")
    '''database_loader.load_to_db("categories", categories_df)
    
    database_loader.load_to_db("countries", countries_df)
    database_loader.load_to_db("cities", cities_df)
    
    database_loader.load_to_db("customers", customers_df)
    database_loader.load_to_db("employees", employees_df)
    
    database_loader.load_to_db("products", products_df)'''
    database_loader.load_to_db("sales", sales_df)
    
    print("ETL process completed successfully.")

if __name__ == "__main__":
    main()
