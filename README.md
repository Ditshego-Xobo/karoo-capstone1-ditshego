# Karoo Agriculture Capstone Project

## Project Overview

This project was created for the Karoo Organics Q4 Performance Report.

The purpose of the project is to automate regional sales reporting using PostgreSQL and Python instead of manual Excel reporting.

The system stores supplier information, orders, sales targets, harvest records, and certifications. Python is then used to automatically generate a quarterly performance report.

---

# Technologies Used

- PostgreSQL
- Python
- pandas
- psycopg2
- VS Code
- pgAdmin 4

---

# Files Included

## schema.sql
This file creates all database tables and relationships.

## load_data.py
This script loads CSV data into PostgreSQL and inserts additional records required for the project.

## analytics.sql
This file contains analytical SQL queries for:
- regional performance against targets
- top suppliers per region

## generate_q4_report.py
This script runs the final automated report and exports results to CSV.

## q4_performance.csv
Generated report showing Q4 regional performance.

---

# Database Tables

The project uses the following tables:

- Suppliers
- Orders
- Sales_Targets
- Certifications
- Harvest_Log

---

# Features Implemented

- Primary Keys
- Foreign Keys
- NOT NULL constraints
- CSV data loading
- Analytical SQL queries
- Ranking using RANK()
- GROUP BY and CASE statements
- Python database automation
- CSV report generation
- Error handling and connection cleanup

---

# How to Run the Project

## 1. Create the database

```sql
CREATE DATABASE karoo_capstone;
```

## 2. Run schema.sql

Run the schema.sql file in pgAdmin.

## 3. Install required packages

```bash
pip install psycopg2-binary pandas
```

## 4. Load the data

```bash
python load_data.py
```

## 5. Generate the report

```bash
python generate_q4_report.py
```

---

# Author

Ditshego Malepe