-- models/marts/dim_assets.sql
WITH holdings AS (
    SELECT * FROM {{ ref('stg_holdings') }}
),
ratings AS (
    SELECT * FROM {{ ref('stg_credit_ratings') }}
)

SELECT
    h.isin,
    h.issuer_name,
    h.asset_type,
    h.sector,
    h.country,
    h.coupon_rate_pct,
    h.maturity_date,
    r.moodys_rating,
    r.sp_rating,
    r.fitch_rating,
    r.rating_outlook,
    -- Decomplexifying for business users
    CASE 
        WHEN r.sp_rating IN ('AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-') THEN 'Investment Grade'
        WHEN r.moodys_rating IN ('Aaa', 'Aa1', 'Aa2', 'Aa3', 'A1', 'A2', 'A3', 'Baa1', 'Baa2', 'Baa3') THEN 'Investment Grade'
        ELSE 'High Yield'
    END AS internal_rating_class
FROM holdings h
LEFT JOIN ratings r ON h.isin = r.isin
-- make sure only one record per asset
QUALIFY ROW_NUMBER() OVER (PARTITION BY h.isin ORDER BY h.valuation_date DESC) = 1
