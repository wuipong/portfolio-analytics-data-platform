def normalize_portfolio(holdings_df, fx_df):
    # 1. Filter currency rate (quote currency in USD)
    # COMMENT: In PySpark use: fx_df.filter(F.col("quote_currency") == "USD")
    usd_rates = fx_df[fx_df['quote_currency'] == 'USD'][['base_currency', 'fx_rate']]
    
    # 2. Normalize
    # LEFT JOIN and convert USD
    normalized = holdings_df.merge(usd_rates, left_on='currency', right_on='base_currency', how='left')
    
    # IF base currency is USD，rate = 1.0
    normalized['fx_rate'] = normalized['fx_rate'].fillna(1.0)
    
    # calculate market value
    normalized['market_value_usd'] = normalized['market_value'] * normalized['fx_rate']
    
    # 3. Standardizing Attributes
    # Convert credit grading to 2 tier levels (Investment Grade vs High Yield)
    # COMMENT: In Databricks use F.when().otherwise()
    normalized['rating_category'] = normalized['credit_rating'].apply(
        lambda x: 'Investment Grade' if any(grade in str(x) for grade in ['AAA', 'AA', 'A', 'BBB']) else 'High Yield'
    )
    
    # COMMENT: in Databricks export into Silver Table
    # normalized.write.format("delta").mode("overwrite").saveAsTable("silver.normalized_holdings")
    
    print("Normalization complete: All holdings converted to USD.")
    return normalized
