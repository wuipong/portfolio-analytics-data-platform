SELECT
    isin,
    CAST(valuation_date AS DATE) AS valuation_date,
    market_price,
    spread,
    yield_to_maturity
FROM {{ source('bronze', 'market_prices') }}
