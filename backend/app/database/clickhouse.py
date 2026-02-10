from etl.load.clickhouse_loader import get_clickhouse_client

def clickhouse_client():
    return get_clickhouse_client()