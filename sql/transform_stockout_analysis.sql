CREATE OR REPLACE VIEW vw_category_availability AS
SELECT
    platform,
    city,
    searched_category,
    COUNT(*) AS products_available,
    ROUND(AVG(price)::numeric, 2) AS avg_price,
    SUM(CASE WHEN has_discount THEN 1 ELSE 0 END) AS discounted_count,
    ROUND(100.0 * SUM(CASE WHEN has_discount THEN 1 ELSE 0 END) / COUNT(*), 1) AS discount_pct
FROM stg_quick_commerce_prices
GROUP BY platform, city, searched_category
ORDER BY products_available ASC;