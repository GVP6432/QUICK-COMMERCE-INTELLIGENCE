CREATE TABLE IF NOT EXISTS stg_quick_commerce_prices (
    id SERIAL PRIMARY KEY,
    name TEXT,
    size TEXT,
    price NUMERIC,
    has_discount BOOLEAN,
    searched_category TEXT,
    pincode TEXT,
    city TEXT,
    platform TEXT,
    scraped_at TIMESTAMP
);