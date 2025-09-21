import pyodbc
import yaml
from pathlib import Path

# Load config
config_path = Path(__file__).resolve().parent.parent.parent / "env.yaml"
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

db_conf = config["sqlserver"]

# Enable pooling global
pyodbc.pooling = True

def get_connection():
    return pyodbc.connect(
        f"DRIVER={db_conf['driver']};"
        f"SERVER=np:{db_conf['pipe']};"
        f"DATABASE={db_conf['database']};"
        f"UID={db_conf['uid']};"
        f"PWD={db_conf['pwd']}"
    )

def run_query(sql: str, skip: int = 0, take: int = 100):
    # Safety check
    if not sql.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    conn = get_connection()
    try:
        cursor = conn.cursor()

        # --- Ambil total count ---
        count_sql = f"SELECT COUNT(*) FROM ({sql}) AS subquery"
        cursor.execute(count_sql)
        total_count = cursor.fetchone()[0]

        # --- Query ambil data (pakai TOP + slicing manual) ---
        limit = skip + take
        query_with_top = f"SELECT TOP {limit} * FROM ({sql}) AS subquery"
        cursor.execute(query_with_top)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        # slicing manual
        sliced_rows = rows[skip:skip+take]
        result_rows = [dict(zip(columns, r)) for r in sliced_rows]

        return {
            "columns": columns,
            "rows": result_rows,
            "totalCount": total_count   # total asli dari COUNT(*)
        }

    finally:
        conn.close()
