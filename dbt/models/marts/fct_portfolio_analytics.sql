WITH enriched AS (SELECT * FROM {{ ref('int_daily_positions_enriched') }}),
portfolio_totals AS (
    SELECT 
        valuation_date, 
        portfolio_id, 
        SUM(market_value_usd) AS total_portfolio_mv 
    FROM enriched 
    GROUP BY 1, 2
)

SELECT
    e.valuation_date,
    e.portfolio_id,
    e.isin,
    e.market_value_usd,
    -- weighting calculation (Automated portfolio analysis)
    e.market_value_usd / t.total_portfolio_mv AS portfolio_weight,
    -- Calculate Duration Contribution
    e.duration * (e.market_value_usd / t.total_portfolio_mv) AS duration_contribution,
    e.yield_to_maturity
FROM enriched e
JOIN portfolio_totals t ON e.portfolio_id = t.portfolio_id AND e.valuation_date = t.valuation_date
