WITH holdings AS (SELECT * FROM {{ ref('stg_holdings') }}),
prices AS (SELECT * FROM {{ ref('stg_market_prices') }}),
fx AS (SELECT * FROM {{ ref('stg_fx_rates') }} WHERE quote_currency = 'USD')

SELECT
    h.*,
    p.market_price AS latest_market_price,
    p.yield_to_maturity,
    COALESCE(f.fx_rate, 1.0) AS usd_fx_rate,
    -- adjusted market value in USD
    (h.market_value * COALESCE(f.fx_rate, 1.0)) AS market_value_usd
FROM holdings h
LEFT JOIN prices p ON h.isin = p.isin AND h.valuation_date = p.valuation_date
LEFT JOIN fx f ON h.currency = f.base_currency AND h.valuation_date = f.valuation_date
