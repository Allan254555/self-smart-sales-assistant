import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_sales():
    sales = pd.read_csv(os.path.join(BASE_DIR,"data","sales.csv"))
    return sales

def load_categories():
    categories = pd.read_csv(os.path.join(BASE_DIR,"data","categories.csv"))
    return categories

def load_products():
    products = pd.read_csv(os.path.join(BASE_DIR,"data","products.csv"))
    
    return products

def load_customers():
    customers = pd .read_csv(os.path.join(BASE_DIR,"data","customers.csv"))
    return customers

def load_cities():
    cities = pd.read_csv(os.path.join(BASE_DIR,"data","cities.csv"))
    return cities
def load_employees():
    employees = pd.read_csv(os.path.join(BASE_DIR,"data","employees.csv"))
    return employees
def load_countries():
    countries = pd.read_csv(os.path.join(BASE_DIR,"data","countries.csv"))
    return countries