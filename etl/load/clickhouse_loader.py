import clickhouse_connect

def get_clickhouse_client():
    return clickhouse_connect.get_client(
        host="localhost",
        port=8123,
        username="allan",
        password="AllanAvosa254!",
        database="store_sales"        
    )

def load_dataframe(client, table_name, df, truncate=True):
    if truncate:
        client.command(f"TRUNCATE TABLE {table_name}")
    client.insert_df(table_name, df)
