SELECT
    portfolio_id,
    CAST(valuation_date AS DATE) AS valuation_date,
    isin,
    issuer_name,
    asset_type,
    currency,
    CAST(market_value AS DECIMAL(18,2)) AS market_value,
    CAST(clean_price AS DECIMAL(18,4)) AS clean_price,
    coupon_rate / 100 AS coupon_rate_pct, -- convert to decimal
    CAST(maturity_date AS DATE) AS maturity_date,
    duration,
    sector,
    country,
    _ingested_at
FROM {{ source('bronze', 'portfolio_holdings') }}
