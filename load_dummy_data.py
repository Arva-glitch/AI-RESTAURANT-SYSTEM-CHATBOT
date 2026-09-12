"""
load_dummy_data.py
------------------
Loads dummy_data.json into the `restaurantsystem` MySQL database.

Usage:
    pip install mysql-connector-python
    python load_dummy_data.py --password YOUR_MYSQL_PASSWORD

Options:
    --host / --port / --user / --password / --database
    --json      path to dummy_data.json (default: ./dummy_data.json)
    --truncate  wipe all target tables before inserting
    --dry-run   print what would happen, insert nothing
"""

import argparse
import json
import sys

try:
    import mysql.connector as mysql
    from mysql.connector import Error as MySQLError
except ImportError:
    sys.exit("Missing driver. Run:  pip install mysql-connector-python")


# Parent tables first — this order satisfies every foreign key in the schema.
TABLE_ORDER = [
    "restaurantdescriptions",
    "categories",
    "customers",
    "addresses",
    "diningtables",
    "menu",
    "coupons",
    "offers",
    "staffs",
    "inventorys",
    "bookings",
    "orders",
    "orderitems",
    "bills",
    "payments",
    "reviews",
    "customer_favourites",
    "user_history",
    "chatbot_conversations",
    "chatbot_sessions",
]

# Columns stored as MySQL JSON — dicts/lists must be serialised before insert.
JSON_COLUMNS = {("chatbot_sessions", "context")}


def prepare(table, row):
    """Return (columns, values) with JSON columns serialised."""
    cols, vals = [], []
    for col, val in row.items():
        if (table, col) in JSON_COLUMNS and not isinstance(val, (str, type(None))):
            val = json.dumps(val)
        cols.append(col)
        vals.append(val)
    return cols, vals


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="localhost")
    p.add_argument("--port", type=int, default=3306)
    p.add_argument("--user", default="root")
    p.add_argument("--password", default="")
    p.add_argument("--database", default="restaurantsystem")
    p.add_argument("--json", default="dummy_data.json")
    p.add_argument("--truncate", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    with open(args.json, encoding="utf-8") as f:
        data = json.load(f)

    if args.dry_run:
        for t in TABLE_ORDER:
            print(f"{t:28} {len(data.get(t, [])):5} rows")
        print("\nDry run — nothing written.")
        return

    conn = mysql.connect(
        host=args.host, port=args.port, user=args.user,
        password=args.password, database=args.database,
    )
    cur = conn.cursor()

    try:
        if args.truncate:
            print("Truncating tables...")
            cur.execute("SET FOREIGN_KEY_CHECKS = 0")
            for t in reversed(TABLE_ORDER):
                cur.execute(f"TRUNCATE TABLE `{t}`")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1")
            conn.commit()

        total = 0
        for table in TABLE_ORDER:
            rows = data.get(table, [])
            if not rows:
                print(f"{table:28} skipped (no rows)")
                continue

            cols, _ = prepare(table, rows[0])
            col_sql = ", ".join(f"`{c}`" for c in cols)
            placeholders = ", ".join(["%s"] * len(cols))
            sql = f"INSERT INTO `{table}` ({col_sql}) VALUES ({placeholders})"

            values = [prepare(table, r)[1] for r in rows]
            cur.executemany(sql, values)
            conn.commit()

            total += len(rows)
            print(f"{table:28} {len(rows):5} rows inserted")

        print(f"\nDone. {total} rows inserted into `{args.database}`.")

    except MySQLError as e:
        conn.rollback()
        print(f"\nFailed on `{table}`: {e}", file=sys.stderr)
        print("Nothing from this table was committed. Fix the issue and re-run.", file=sys.stderr)
        sys.exit(1)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
