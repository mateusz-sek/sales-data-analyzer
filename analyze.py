import sqlite3
import pandas as pd

raw_data = [
    {"order_id": 101, "product": "Laptop", "amount": 3500.0, "status": "Paid"},
    {"order_id": 102, "product": "Mouse", "amount": 120.0, "status": "Paid"},
    {"order_id": 103, "product": "Monitor", "amount": -500.0, "status": "Error"},
    {"order_id": 104, "product": "Laptop", "amount": 3500.0, "status": "Paid"},
    {"order_id": 105, "product": "Keyboard", "amount": None, "status": "Cancelled"}
]

df = pd.DataFrame(raw_data)

clean_df = df.dropna(subset=["amount"])
clean_df = clean_df[clean_df["amount"] > 0]

conn = sqlite3.connect("sales.db")
clean_df.to_sql("orders", conn, if_exists="replace", index=False)

report = pd.read_sql_query("""
    SELECT product, COUNT(*) AS quantity, SUM(amount) AS total_revenue
    FROM orders
    GROUP BY product
    ORDER BY total_revenue DESC
""", conn)

print("=== SALES REPORT (SQL) ===")
print(report)
conn.close()
