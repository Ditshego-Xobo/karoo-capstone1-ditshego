# Karoo Organics Capstone Project
# This script creates the final Q4 report automatically.
# It connects to PostgreSQL, runs the report queries,
# saves the main report as a CSV file, and prints a short summary.

import psycopg2
import pandas as pd


def connect_to_database():
    """Connect Python to the PostgreSQL database."""
    return psycopg2.connect(
        host="localhost",
        database="karoo_capstone",
        user="postgres",
        password="*****",
        port="5432"
    )


def main():
    conn = None

    try:
        conn = connect_to_database()

        regional_query = """
            SELECT
                s.region,
                SUM(o.total_price) AS actual_revenue,
                st.target_amount,
                CASE
                    WHEN st.target_amount = 0 THEN 0
                    ELSE ROUND((SUM(o.total_price) / st.target_amount) * 100, 2)
                END AS percentage_of_target
            FROM Suppliers s
            JOIN Orders o
                ON s.supplier_id = o.supplier_id
            JOIN Sales_Targets st
                ON s.region = st.region
            WHERE st.quarter = '2025-Q4'
            GROUP BY s.region, st.target_amount
            ORDER BY percentage_of_target DESC;
        """

        ranking_query = """
            SELECT
                region,
                farm_name,
                total_revenue,
                regional_rank
            FROM (
                SELECT
                    s.region,
                    s.farm_name,
                    SUM(o.total_price) AS total_revenue,
                    RANK() OVER (
                        PARTITION BY s.region
                        ORDER BY SUM(o.total_price) DESC
                    ) AS regional_rank
                FROM Suppliers s
                JOIN Orders o
                    ON s.supplier_id = o.supplier_id
                GROUP BY s.region, s.farm_name
            ) ranked_suppliers
            WHERE regional_rank <= 3
            ORDER BY region, regional_rank;
        """

        regional_report = pd.read_sql_query(regional_query, conn)
        supplier_ranking = pd.read_sql_query(ranking_query, conn)

        regional_report.to_csv("q4_performance.csv", index=False)

        print("Q4 performance report created successfully.")
        print("The file q4_performance.csv has been saved in this project folder.")
        print()
        print("Regional Performance Summary:")
        print(regional_report)
        print()
        print("Top Suppliers by Region:")
        print(supplier_ranking)

    except Exception as error:
        print("An error happened while generating the report.")
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
