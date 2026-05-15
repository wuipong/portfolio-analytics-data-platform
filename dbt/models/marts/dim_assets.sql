SELECT
    isin,
    issuer_name,
    asset_type,
    sector,
    country,
    coupon_rate_pct,
    maturity_date,
    r.moodys_rating,
    r.sp_rating,
    CASE 
        WHEN r.sp_rating IN ('AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-') THEN 'Investment Grade'
        ELSE 'High Yield'
    END AS internal_rating_class
FROM {{ ref('stg_holdings') }} h
LEFT JOIN {{ source('bronze', 'credit_ratings') }} r USING (isin)
GROUP BY 1,2,3,4,5,6,7,8,9,10
