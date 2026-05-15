# main.py
import sys
import subprocess
from src.data_ingestion import ingest_raw_to_bronze
from src.quality_check import DataQualityChecker
from src.normalization import normalize_portfolio

def run_pipeline():
    """
    Orchestrates the end-to-end Portfolio Analytics Pipeline.
    Steps: Ingestion -> Quality Check -> Normalization -> dbt Modeling
    """
    print("="*50)
    print("🚀 Starting Portfolio Analytics ETL Pipeline")
    print("="*50)

    try:
        # STEP 1: Data Ingestion (Bronze Layer)
        print("\n[1/4] Ingesting raw CSV files to Bronze Layer...")
        holdings_df = ingest_raw_to_bronze("portfolio_holdings.csv")
        fx_df = ingest_raw_to_bronze("fx_rates.csv")
        prices_df = ingest_raw_to_bronze("market_prices.csv")
        ratings_df = ingest_raw_to_bronze("credit_ratings.csv")

        # STEP 2: Quality Control (The Gatekeeper)
        print("\n[2/4] Running Automated Quality Checks...")
        dq = DataQualityChecker(holdings_df, prices_df)
        if not dq.run_checks():
            print("❌ Pipeline Halted: Data quality exceptions found.")
            sys.exit(1) # return for Airflow capture failure

        # STEP 3: Data Normalization (Silver Layer)
        print("\n[3/4] Normalizing data to Silver Layer (USD Base)...")
        silver_df = normalize_portfolio(holdings_df, fx_df)
        # silver_df.to_csv("data/processed/silver_holdings.csv", index=False)

        # STEP 4: dbt Modeling (Gold Layer)
        print("\n[4/4] Executing dbt transformations...")
        # COMMENT: In Databricks/Airflow environment，use BashOperator
        # subprocess.run(["dbt", "run"], check=True)
        # subprocess.run(["dbt", "test"], check=True)

        print("\n" + "="*50)
        print("✅ Pipeline Completed Successfully")
        print("="*50)

    except Exception as e:
        print(f"\n💥 Pipeline Failed with error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
