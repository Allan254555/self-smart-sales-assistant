import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()
def create_dataframe():
    data= {
        'names':['Alice','Bob','Charlie','David','Eve'],
        'age':[23,45,54,20,12],
        'initials':['A','B','C','D','E']     
        
    }
    df = pd.DataFrame(data)
    print(df.dtypes)
    return df

def load_to_database(df,user,password,host,port,database,table_name):
    db_url=f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(db_url)
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
def main():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    table_name =os.getenv("Table")

    
    df = create_dataframe()
    print("Dataframe Created Successfully")
    
    load_to_database(df,user,password,host,port,database,table_name)
    
if __name__ == "__main__":
    main()