from etl.extract import load_data
from etl.load import clickhouse_loader
from etl.transform import (
    categories_processing,
    cities_processing,
    countries_processing,
    customers_processing,
    employees_processing,
    products_processing,
    sales_data_processing
)

    

#from etl.load import clickhouse_loader
import pandas as pd


def main():
    print("=== Starting ETL Pipeline ===")

    client = clickhouse_loader.get_clickhouse_client()

    print("Extracting data...")
    categories = load_data.load_categories()
    cities = load_data.load_cities()
    countries = load_data.load_countries()    
    customers = load_data.load_customers()
    employees = load_data.load_employees()

    products = load_data.load_products()
    sales = load_data.load_sales()
    
   
  
    print("Transforming data...")
    categories_df = categories_processing.clean_data(categories)
    cities_df = cities_processing.clean_data(cities)
    countries_df = countries_processing.clean_data(countries)
    customers_df = customers_processing.clean_data(customers)
    employees_df = employees_processing.clean_data(employees)
    
    products_df = products_processing.clean_data(products)
    sales_df = sales_data_processing.clean_data(sales,products_df)


    print("Loading data into the database...")
    clickhouse_loader.load_dataframe(client,"countries", countries_df)
    clickhouse_loader.load_dataframe(client,"cities", cities_df)

    clickhouse_loader.load_dataframe(client,"categories", categories_df)
    clickhouse_loader.load_dataframe(client,"products", products_df)    
    
    clickhouse_loader.load_dataframe(client,"customers", customers_df)
    clickhouse_loader.load_dataframe(client,"employees", employees_df)
       
    clickhouse_loader.load_dataframe(client,"sales", sales_df)
    
   
    
    print("ETL process completed successfully.")

if __name__ == "__main__":
    main()
