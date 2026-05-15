class DataQualityChecker:
    def __init__(self, holdings_df, prices_df):
        self.holdings = holdings_df
        self.prices = prices_df

    def run_checks(self):
        # 1. Missing Price Check
        # Check Missing ISIN 
        missing_isin = self.holdings[~self.holdings['isin'].isin(self.prices['isin'])]
        
        # 2. Outlier Check
        # example bond price should between 50 - 150
        # COMMENT: In Databricks use PySpark: df.filter((F.col("clean_price") < 50) | (F.col("clean_price") > 150))
        price_outliers = self.holdings[(self.holdings['clean_price'] < 50) | (self.holdings['clean_price'] > 150)]
        
        # 3. abnormal data notification
        errors_found = False
        if len(missing_isin) > 0:
            print(f"CRITICAL: Found {len(missing_isin)} assets with missing market prices!")
            errors_found = True
        
        if len(price_outliers) > 0:
            print(f"WARNING: Found {len(price_outliers)} price outliers outside [50, 150] range.")
            errors_found = True
            
        if not errors_found:
            print("Data Quality Checks Passed: No exceptions found.")
        
        # COMMENT: In production (Databricks/Airflow)，if errors_found is True，trigger raise Exception and terminate workdlows
        return not errors_found

# COMMENT: In Databricks，usually read data from Table：
# holdings_df = spark.table("bronze.portfolio_holdings")
