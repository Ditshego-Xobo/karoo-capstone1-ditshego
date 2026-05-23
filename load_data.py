# Karoo Organics Capstone Project
# This script loads the CSV data into PostgreSQL.
# It also adds extra harvest, certification, and order records
# so that the database has enough data for the Q4 report.

import psycopg2
import pandas as pd


def connect_to_database():
    """
    This function connects Python to my PostgreSQL database.
    I kept the connection details in one place so they are easier to change.
    """
    conn = psycopg2.connect(
        host="localhost",
        database="karoo_capstone",
        user="postgres",
        password="Masobo@2025",
        port="5432"
    )
    return conn


def load_suppliers(cursor):
    """
    This function reads suppliers.csv and inserts supplier records.
    """
    suppliers = pd.read_csv("suppliers.csv")

    for index, row in suppliers.iterrows():
        cursor.execute("""
            INSERT INTO Suppliers (supplier_id, farm_name, region)
            VALUES (%s, %s, %s)
            ON CONFLICT (supplier_id) DO NOTHING;
        """, (
            int(row["supplier_id"]),
            row["farm_name"],
            row["region"]
        ))


def load_orders(cursor):
    """
    This function reads orders.csv and inserts order records.
    The CSV file only has order_id, supplier_id, order_date, and total_price.
    """
    orders = pd.read_csv("orders.csv")

    for index, row in orders.iterrows():
        cursor.execute("""
            INSERT INTO Orders (order_id, supplier_id, product_name, quantity, total_price, order_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (order_id) DO NOTHING;
        """, (
            int(row["order_id"]),
            int(row["supplier_id"]),
            "Mixed Produce",
            1,
            float(row["total_price"]),
            row["order_date"]
        ))


def load_targets(cursor):
    """
    This function reads targets.csv and inserts the regional sales targets.
    """
    targets = pd.read_csv("targets.csv")

    for index, row in targets.iterrows():
        cursor.execute("""
            INSERT INTO Sales_Targets (region, quarter, target_amount)
            VALUES (%s, %s, %s)
            ON CONFLICT (region, quarter) DO NOTHING;
        """, (
            row["region"],
            row["quarter"],
            float(row["target_amount"])
        ))


def insert_extra_records(cursor):
    """
    This function inserts extra records required by the project.
    These include harvest records, certification records, and extra Q4 orders.
    """

    cursor.execute("""
        INSERT INTO Harvest_Log (supplier_id, crop_name, harvest_date, quantity_harvested)
        VALUES
            (1, 'Lamb', '2025-10-03', 120),
            (2, 'Dates', '2025-10-10', 200),
            (3, 'Wool', '2025-11-01', 150),
            (4, 'Grapes', '2025-11-15', 300),
            (5, 'Olives', '2025-12-01', 250)
        ON CONFLICT DO NOTHING;
    """)

    cursor.execute("""
        INSERT INTO Certifications (supplier_id, certification_name, issue_date)
        VALUES
            (1, 'Organic Farming Certificate', '2025-01-15'),
            (3, 'Sustainable Agriculture Certificate', '2025-02-20'),
            (4, 'Fair Trade Certificate', '2025-03-10')
        ON CONFLICT DO NOTHING;
    """)

    cursor.execute("""
        INSERT INTO Orders (order_id, supplier_id, product_name, quantity, total_price, order_date)
        VALUES
            (12, 1, 'Lamb', 10, 6500.00, '2025-12-05'),
            (13, 2, 'Dates', 20, 7200.00, '2025-12-07'),
            (14, 4, 'Grapes', 30, 11000.00, '2025-12-10'),
            (15, 5, 'Olives', 25, 8800.00, '2025-12-12')
        ON CONFLICT (order_id) DO NOTHING;
    """)


def main():
    conn = None

    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        load_suppliers(cursor)
        load_orders(cursor)
        load_targets(cursor)
        insert_extra_records(cursor)

        conn.commit()

        print("Data was loaded successfully.")
        print("Suppliers, orders, sales targets, harvest records, and certifications are now in the database.")

    except Exception as error:
        print("Something went wrong while loading the data.")
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()