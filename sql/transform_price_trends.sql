CREATE OR REPLACE VIEW vw_price_comparison AS
WITH platform_counts AS (
    SELECT
        name_key,
        size_key,
        city,
        COUNT(DISTINCT platform) AS platforms_matched
    FROM stg_quick_commerce_prices
    GROUP BY name_key, size_key, city
)
SELECT
    s.name_key,
    s.size_key,
    s.city,
    s.searched_category,
    s.name,
    s.platform,
    s.price,
    s.has_discount,
    pc.platforms_matched,
    RANK() OVER (
        PARTITION BY s.name_key, s.size_key, s.city
        ORDER BY s.price ASC
    ) AS price_rank
FROM stg_quick_commerce_prices s
JOIN platform_counts pc
    ON s.name_key = pc.name_key
    AND s.size_key = pc.size_key
    AND s.city = pc.city;