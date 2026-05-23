-- Karoo Organics Capstone Project
-- This file creates the database tables needed for the Q4 regional report.
-- The tables store supplier details, customer orders, sales targets,
-- certifications, and harvest records.

-- This table stores the farms/suppliers that sell products to Karoo Organics.
CREATE TABLE Suppliers (
    supplier_id INT PRIMARY KEY,
    farm_name VARCHAR(100) NOT NULL,
    owner_name VARCHAR(100),
    region VARCHAR(50) NOT NULL
);

-- This table stores order information.
-- Each order is linked to one supplier using supplier_id.
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    supplier_id INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    order_date DATE NOT NULL,

    CONSTRAINT fk_orders_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES Suppliers(supplier_id)
);

-- This table stores the sales target for each region and quarter.
-- I used region and quarter together as the primary key because
-- each region should only have one target per quarter.
CREATE TABLE Sales_Targets (
    region VARCHAR(50) NOT NULL,
    quarter VARCHAR(10) NOT NULL,
    target_amount DECIMAL(12,2) NOT NULL,

    PRIMARY KEY (region, quarter)
);

-- This table stores organic or product certifications for suppliers.
CREATE TABLE Certifications (
    certification_id SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL,
    certification_name VARCHAR(100) NOT NULL,
    issue_date DATE NOT NULL,

    CONSTRAINT fk_cert_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES Suppliers(supplier_id)
);

-- This table stores harvest records.
-- It helps show what crops were harvested and by which supplier.
CREATE TABLE Harvest_Log (
    harvest_id SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL,
    crop_name VARCHAR(100) NOT NULL,
    harvest_date DATE NOT NULL,
    quantity_harvested INT NOT NULL,

    CONSTRAINT fk_harvest_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES Suppliers(supplier_id)
);