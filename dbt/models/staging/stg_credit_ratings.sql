-- models/staging/stg_credit_ratings.sql
SELECT
    isin,
    moodys_rating,
    sp_rating,
    fitch_rating,
    rating_outlook,
    CASE 
        WHEN moodys_rating IS NULL AND sp_rating IS NULL AND fitch_rating IS NULL THEN 'Missing'
        ELSE 'Active'
    END AS rating_status,
    _ingested_at
FROM {{ source('bronze', 'credit_ratings') }}
