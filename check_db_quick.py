import sqlite3
import os

db_path = "governance_weekly/data/gov_weekly.db"
print(f"DB Path: {db_path}")
print(f"DB exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # List tables
    tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print(f"Tables: {tables}")
    
    # Count articles
    try:
        count = cur.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
        print(f"Total articles: {count}")
        
        # Show sample if any exist
        if count > 0:
            print("\nSample articles:")
            rows = cur.execute("SELECT url, source_domain, title_original FROM articles LIMIT 5").fetchall()
            for r in rows:
                print(f"  - {r[1]}: {r[2][:60] if r[2] else 'No title'}...")
        else:
            print("\n*** DATABASE IS EMPTY - No articles have been scraped yet ***")
    except Exception as e:
        print(f"Error: {e}")
    
    conn.close()
else:
    print("Database file does not exist yet!")
