import sqlite3

# Database file path
db_path = "/data/ticket-sales.db"

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# SQL query to calculate total sales for "Gold" ticket type
cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold';")
total_sales = cursor.fetchone()[0]  # Fetch result

# Ensure total_sales is not None (handle case where no records exist)
total_sales = total_sales if total_sales else 0

# Write the result to /data/ticket-sales-gold.txt
with open("/data/ticket-sales-gold.txt", "w") as f:
    f.write(str(total_sales))

# Close connection
conn.close()
