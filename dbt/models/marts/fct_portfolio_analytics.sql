{{ config(materialized='table') }}

WITH silver_data AS (
    SELECT * FROM {{ source('silver', 'int_normalized_holdings') }}
    WHERE Quality_Flag = 'CLEAN'
),

ratings AS (
    SELECT * FROM {{ ref('stg_credit_ratings') }}
),

total_sum AS (
    SELECT SUM(MarketValue_USD) as total_mv FROM silver_data
)

SELECT
    s.AsOfDate,
    s.ISIN,
    s.AssetType,
    s.MarketValue_USD,
    -- 計算資產權重 (Key Performance Area: Quantitative analysis)
    (s.MarketValue_USD / t.total_mv) as Portfolio_Weight,
    r.Rating_Provider,
    r.Credit_Rating,
    -- 映射評級分數以進行數值化風險分析
    CASE 
        WHEN r.Credit_Rating = 'AAA' THEN 1
        WHEN r.Credit_Rating = 'AA' THEN 2
        ELSE 10 
    END as Rating_Score
FROM silver_data s
CROSS JOIN total_sum t
LEFT JOIN ratings r ON s.ISIN = r.ISIN
