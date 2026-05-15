# main.py
from src.data_ingestion import ingest_raw_to_bronze
from src.quality_check import DataQualityChecker
from src.normalization import normalize_portfolio

def run_pipeline():
    print("--- Execute Portfolio Analytics ETL Pipeline ---")

    # STEP 1: Ingestion
    print("\n[Step 1/3] Ingest raw data to bronze layer...")
    holdings_df = ingest_raw_to_bronze("portfolio_holdings.csv")
    fx_df = ingest_raw_to_bronze("fx_rates.csv")
    prices_df = ingest_raw_to_bronze("market_prices.csv")
    ratings_df = ingest_raw_to_bronze("credit_ratings.csv")

    # STEP 2: Quality Check
    print("\n[Step 2/3] Execute Quality Checks...")
    dq_checker = DataQualityChecker(holdings_df, prices_df)
    
    if not dq_checker.run_checks():
        # If check fail, terminate Pipeline and alert
        print("CRITICAL: quality check failed, Pipeline terminate。")
        return 

    # STEP 3: Normalization (Silver Layer)
    print("\n[Step 3/3] Normalization...")
    silver_df = normalize_portfolio(holdings_df, fx_df)

    # Final export
    print("\n--- Pipeline succeed ---")
    print(f"final line number ingested: {len(silver_df)}")
    # silver_df.to_csv("data/processed/final_holdings_usd.csv", index=False)

if __name__ == "__main__":
    run_pipeline()
