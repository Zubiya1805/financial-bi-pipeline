CREATE TABLE dim_region(
    region_id INT PRIMARY KEY AUTO_INCREMENT,
    region_name VARCHAR(100) NOT NULL
);

CREATE TABLE dim_segment(
    segment_id INT PRIMARY KEY AUTO_INCREMENT,
    segement_name VARCHAR(100) NOT NULL
);

CREATE TABLE dim_product(
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    product_category VARCHAR(100) NOT NULL
);

CREATE TABLE fact_transactions(
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_date DATE NOT NULL,
    region_id INT,
    segment_id INT,
    product_id INT,
    sales_amount DECIMAL(10, 2) NOT NULL,
    quantity_sold INT NOT NULL,
    discount DECIMAL(5, 2) NOT NULL,
    profit DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id),
    FOREIGN KEY (segment_id) REFERENCES dim_segment(segment_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id)
);