import sqlite3
import csv
from pathlib import Path
import shutil

# config
CSV_DIR = Path("output")
PROCESSED_DIR = Path("processed")
DB_FILE = "data.db"
#

def init_db(): # open or create the db and check for users table
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
      user_id          TEXT PRIMARY KEY,
      first_name       TEXT,
      last_name        TEXT,
      email            TEXT,
      signup_date      TEXT,
      last_login       TEXT,
      age              INTEGER,
      country          TEXT,
      is_active        INTEGER,
      account_balance  REAL,
      num_logins       INTEGER,
      feedback_score   REAL,
      purchase_count   INTEGER,
      subscription_type TEXT,
      referral_source  TEXT          
    )""")
    conn.commit()
    return conn

def ingest_csv(path: Path, conn: sqlite3.Connection): # read one csv and move it to processed directory
    print(f"→ ingesting {path.name} …")
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for r in reader:
            rows.append((
                r["user_id"],
                r["first_name"],
                r["last_name"],
                r["email"],
                r["signup_date"],
                r["last_login"],
                int(r["age"]),
                r["country"],
                1 if r["is_active"].lower() in ("true","1") else 0,
                float(r["account_balance"]),
                int(r["num_logins"]),
                float(r["feedback_score"]),
                int(r["purchase_count"]),
                r["subscription_type"],
                r["referral_source"]    
            ))
    c = conn.cursor()
    c.executemany("""
      INSERT OR IGNORE INTO users VALUES (
        ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
      )
    """, rows)
    conn.commit()

    # now move the file
    target = PROCESSED_DIR / path.name 
    shutil.move(str(path), str(target))
    print(f"  moved → {target}")

def main():
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    conn = init_db()

    for csv_path in sorted(CSV_DIR.glob("*.csv")):
        ingest_csv(csv_path, conn)

    conn.close()
    print("✓ all done.")

if __name__ == "__main__":
    main()  