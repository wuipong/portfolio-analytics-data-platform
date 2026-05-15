SELECT
    base_currency,
    quote_currency,
    fx_rate,
    CAST(valuation_date AS DATE) AS valuation_date
FROM {{ source('bronze', 'fx_rates') }}
