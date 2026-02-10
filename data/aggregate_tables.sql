
'''
Monthly product sales
Answers: top products, product trends, product comparisons over time
'''

CREATE TABLE IF NOT EXISTS monthly_product_sales
(
    year_month UInt32,
    productid UInt32,
    total_quantity UInt64,
    total_revenue Float64,
    transactions UInt64, sh
    avg_discount Float64
)
ENGINE = SummingMergeTree
PARTITION BY year_month
ORDER BY (year_month, productid);

TRUNCATE TABLE monthly_product_sales;

INSERT INTO monthly_product_sales
SELECT
    toYYYYMM(salesdate) AS year_month,
    productid,
    sum(quantity) AS total_quantity,
    sum(totalprice) AS total_revenue,
    uniqExact(transactionnumber) AS transactions,
    avg(discount) AS avg_discount
FROM sales
GROUP BY year_month, productid;

'''
Daily product sales (spikes + anomaly detection)
Answers: daily trends, unusual changes, stock planning signals
'''

CREATE TABLE IF NOT EXISTS daily_product_sales
(
    sales_day Date,
    productid UInt32,
    total_quantity UInt64,
    total_revenue Float64,
    transactions UInt64,
    avg_discount Float64
)
ENGINE = SummingMergeTree
PARTITION BY toYYYYMM(sales_day)
ORDER BY (sales_day, productid);

TRUNCATE TABLE daily_product_sales;

INSERT INTO daily_product_sales
SELECT
    toDate(salesdate) AS sales_day,
    productid,
    sum(quantity) AS total_quantity,
    sum(totalprice) AS total_revenue,
    uniqExact(transactionnumber) AS transactions,
    avg(discount) AS avg_discount
FROM sales
GROUP BY sales_day, productid;

'''
Monthly category sales (category performance)
Answers: which category sells more, category trends
'''
CREATE TABLE IF NOT EXISTS monthly_category_sales
(
    year_month UInt32,
    categoryid UInt32,
    total_quantity UInt64,
    total_revenue Float64,
    transactions UInt64,
    avg_discount Float64
)
ENGINE = SummingMergeTree
PARTITION BY year_month
ORDER BY (year_month, categoryid);

TRUNCATE TABLE monthly_category_sales;

INSERT INTO monthly_category_sales
SELECT
    toYYYYMM(s.salesdate) AS year_month,
    p.categoryid AS categoryid,
    sum(s.quantity) AS total_quantity,
    sum(s.totalprice) AS total_revenue,
    uniqExact(s.transactionnumber) AS transactions,
    avg(s.discount) AS avg_discount
FROM sales s
JOIN products p ON s.productid = p.productid
GROUP BY year_month, categoryid;

'''
Monthly salesperson performance
Answers: which salesperson sold more, performance trends, ranking
'''

CREATE TABLE IF NOT EXISTS monthly_salesperson_sales
(
    year_month UInt32,
    salespersonid UInt32,
    total_quantity UInt64,
    total_revenue Float64,
    transactions UInt64,
    avg_discount Float64
)
ENGINE = SummingMergeTree
PARTITION BY year_month
ORDER BY (year_month, salespersonid);

TRUNCATE TABLE monthly_salesperson_sales;

INSERT INTO monthly_salesperson_sales
SELECT
    toYYYYMM(salesdate) AS year_month,
    salespersonid,
    sum(quantity) AS total_quantity,
    sum(totalprice) AS total_revenue,
    uniqExact(transactionnumber) AS transactions,
    avg(discount) AS avg_discount
FROM sales
GROUP BY year_month, salespersonid;

'''
Customer sales summary (lifetime)
Answers: top customers, loyal customers, heavy buyers
'''

CREATE TABLE IF NOT EXISTS customer_sales_summary
(
    customerid UInt32,
    total_revenue Float64,
    total_quantity UInt64,
    total_orders UInt64,
    avg_order_value Float64,
    avg_discount Float64,
    first_purchase Date,
    last_purchase Date,
    active_days UInt32
)
ENGINE = MergeTree
ORDER BY customerid;

TRUNCATE TABLE customer_sales_summary;

INSERT INTO customer_sales_summary
SELECT
    customerid,
    sum(totalprice) AS total_revenue,
    sum(quantity) AS total_quantity,
    uniqExact(transactionnumber) AS total_orders,
    if(uniqExact(transactionnumber) = 0, 0.0, sum(totalprice) / uniqExact(transactionnumber)) AS avg_order_value,
    avg(discount) AS avg_discount,
    min(toDate(salesdate)) AS first_purchase,
    max(toDate(salesdate)) AS last_purchase,
    uniqExact(toDate(salesdate)) AS active_days
FROM sales
GROUP BY customerid;

'''
Monthly customer activity (optional but powerful)
Answers: customer trends over time, retention, reactivation
'''
CREATE TABLE IF NOT EXISTS monthly_customer_sales
(
    year_month UInt32,
    customerid UInt32,
    total_revenue Float64,
    total_quantity UInt64,
    orders UInt64,
    avg_discount Float64
)
ENGINE = SummingMergeTree
PARTITION BY year_month
ORDER BY (year_month, customerid);

TRUNCATE TABLE monthly_customer_sales;

INSERT INTO monthly_customer_sales
SELECT
    toYYYYMM(salesdate) AS year_month,
    customerid,
    sum(totalprice) AS total_revenue,
    sum(quantity) AS total_quantity,
    uniqExact(transactionnumber) AS orders,
    avg(discount) AS avg_discount
FROM sales
GROUP BY year_month, customerid;

'''
Monthly city sales (location analytics)
Answers: best cities, city trends, expansion decisions
'''

CREATE TABLE IF NOT EXISTS monthly_city_sales
(
    year_month UInt32,
    cityid UInt32,
    total_revenue Float64,
    total_quantity UInt64,
    transactions UInt64
)
ENGINE = SummingMergeTree
PARTITION BY year_month
ORDER BY (year_month, cityid);

TRUNCATE TABLE monthly_city_sales;

INSERT INTO monthly_city_sales
SELECT
    toYYYYMM(s.salesdate) AS year_month,
    c.cityid AS cityid,
    sum(s.totalprice) AS total_revenue,
    sum(s.quantity) AS total_quantity,
    uniqExact(s.transactionnumber) AS transactions
FROM sales s
JOIN customers cu ON s.customerid = cu.customerid
JOIN cities c ON cu.cityid = c.cityid
GROUP BY year_month, cityid;

'''
Monthly country sales (location analytics)
Answers: country performance, regional trends
'''
CREATE TABLE IF NOT EXISTS monthly_country_sales
(
    year_month UInt32,
    countryid UInt32,
    total_revenue Float64,
    total_quantity UInt64,
    transactions UInt64
)
ENGINE = SummingMergeTree
PARTITION BY year_month
ORDER BY (year_month, countryid);

TRUNCATE TABLE monthly_country_sales;

INSERT INTO monthly_country_sales
SELECT
    toYYYYMM(s.salesdate) AS year_month,
    co.countryid AS countryid,
    sum(s.totalprice) AS total_revenue,
    sum(s.quantity) AS total_quantity,
    uniqExact(s.transactionnumber) AS transactions
FROM sales s
JOIN customers cu ON s.customerid = cu.customerid
JOIN cities ci ON cu.cityid = ci.cityid
JOIN countries co ON ci.countryid = co.countryid
GROUP BY year_month, countryid;

