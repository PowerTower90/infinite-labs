import sqlite3
from datetime import datetime, timedelta

db_path = 'instance/peptides.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

try:
    # First, list all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("\nAvailable tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Check which order table exists
    table_name = None
    for table in tables:
        if 'order' in table[0].lower():
            table_name = table[0]
            break
    
    if table_name:
        print(f"\nQuerying table: {table_name}\n")
        # Get recent orders
        query = f"SELECT * FROM [{table_name}] ORDER BY created_at DESC LIMIT 20"
        cursor.execute(query)
        
        rows = cursor.fetchall()
        if rows:
            print("="*100)
            print("RECENT ORDERS - EMAIL DELIVERY CHECK")
            print("="*100 + "\n")
            
            for row in rows:
                print(f"Order ID: {row['id']}")
                print(f"Email: {row['email']}")
                print(f"Status: {row['status']}")
                print(f"Payment Method: {row['payment_method']}")
                print(f"Payment ID: {row['payment_id']}")
                print(f"Created At: {row['created_at']}")
                print("-"*100)
        else:
            print("\nNo orders found in database\n")
    else:
        print("\nNo order table found in database")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
