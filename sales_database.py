# Basic Sales Summary using SQLite and Python

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")


sample_data = [
    ("Laptop", 5, 55000),
    ("Mouse", 25, 800),
    ("Keyboard", 15, 1500),
    ("Monitor", 8, 12000),
    ("Laptop", 3, 56000),
    ("Mouse", 18, 850)
]

cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
conn.commit()


query = """
SELECT 
    product, 
    SUM(quantity) AS total_qty, 
    SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
"""

df = pd.read_sql_query(query, conn)


print("=== Basic Sales Summary ===")
print(df)


plt.figure(figsize=(8, 5))
plt.bar(df["product"], df["revenue"], color='skyblue')
plt.title("Total Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue (₹)")
plt.tight_layout()
plt.show()


plt.savefig("sales_chart.png")

conn.close()
