CREATE OR REPLACE VIEW vw_price_comparison AS
SELECT
    searched_category,
    city,
    name,
    size,
    price,
    has_discount,
    RANK() OVER (
        PARTITION BY searched_category, city, name, size
        ORDER BY price ASC
    ) AS price_rank
FROM stg_quick_commerce_prices
WHERE platform = 'blinkit';