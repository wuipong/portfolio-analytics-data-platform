import sys
import subprocess
import logging
from src.data_ingestion import ingest_raw_to_bronze
from src.quality_check import DataQualityChecker
from src.normalization import normalize_portfolio

# logging for error handling
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    logging.info("Starting Portfolio Analytics ETL Pipeline")
    """
    Orchestrates the end-to-end Portfolio Analytics Pipeline.
    Steps: Ingestion -> Quality Check -> Normalization -> dbt Modeling -> dbt test
    """

    try:
        # STEP 1: Data Ingestion (Bronze Layer)
        logging.info("[1/5] Ingesting raw CSV feeds...")
        holdings_df = ingest_raw_to_bronze("portfolio_holdings.csv")
        fx_df = ingest_raw_to_bronze("fx_rates.csv")
        prices_df = ingest_raw_to_bronze("market_prices.csv")
        ratings_df = ingest_raw_to_bronze("credit_ratings.csv")

        # STEP 2: Quality Control (The Gatekeeper)
        logging.info("[2/5] Running Exception-based Quality Controls...")
        dq = DataQualityChecker(holdings_df, prices_df)
        if not dq.run_checks():
            logging.error("❌ Quality Checks failed. Pipeline Halted.")
            sys.exit(1) # return for Airflow capture failure

        # STEP 3: Data Normalization (Silver Layer)
        logging.info("[3/5] Normalizing currencies and attributes...")
        silver_df = normalize_portfolio(holdings_df, fx_df)
        # silver_df.to_csv("data/processed/silver_holdings.csv", index=False)

        # STEP 4: dbt Modeling (Gold Layer)
        logging.info("[4/5] Executing dbt models (Star Schema)...")
        dbt_run = subprocess.run(["dbt", "run"], capture_output=True, text=True)
        if dbt_run.returncode != 0:
            logging.error(f"❌ dbt Run failed: {dbt_run.stderr}")
            sys.exit(1)
        logging.info(dbt_run.stdout)
        # COMMENT: In Databricks/Airflow environment，use BashOperator
        # subprocess.run(["dbt", "run"], check=True)
        # subprocess.run(["dbt", "test"], check=True)

        # --- STEP 5: dbt Test (Post-Modeling Audit) ---
        logging.info("[5/5] Executing dbt data dictionary tests...")
        dbt_test = subprocess.run(["dbt", "test"], capture_output=True, text=True)
        if dbt_test.returncode != 0:
            logging.warning("⚠️ dbt Tests failed. Data may have consistency issues.")
            logging.warning(dbt_test.stdout)
        else:
            logging.info("✅ All dbt tests passed.")

        logging.info("Pipeline completed.")

    except Exception as e:
        logging.error(f"Pipeline crashed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
