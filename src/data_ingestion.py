import pandas as pd
from datetime import datetime
import os


def ingest_raw_to_bronze(file_name):
    raw_path = f"data/raw/{file_name}"
    
    # 1. read csv 
    # COMMENT: In Databricks , change to spark.read.format("csv").option("header","true").load(path)
    df = pd.read_csv(raw_path)
    
    # 2. Audit Fields
    df['_ingested_at'] = datetime.now()
    df['_source_file'] = file_name
    df['_status'] = 'INGESTED'
    
    # COMMENT: In Databricks , write into Delta Table
    # df.write.format("delta").mode("overwrite").saveAsTable(f"bronze.{file_name.replace('.csv', '')}")
    
    print(f"Successfully ingested {file_name} with audit fields.")
    return df

if __name__ == "__main__":
    if not os.path.exists("data/raw/"):
        os.makedirs("data/raw/")
        
    holdings_df = ingest_raw_to_bronze("portfolio_holdings.csv")
    fx_df = ingest_raw_to_bronze("fx_rates.csv")
    prices_df = ingest_raw_to_bronze("market_prices.csv")
    ratings_df = ingest_raw_to_bronze("credit_ratings.csv")
