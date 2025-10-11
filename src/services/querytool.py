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

        # --- Trim string values ---
        result_rows = []
        for row in sliced_rows:
            clean_row = {}
            for col, val in zip(columns, row):
                if isinstance(val, str):
                    clean_row[col] = val.strip()
                else:
                    clean_row[col] = val
            result_rows.append(clean_row)

        return {
            "columns": columns,
            "rows": result_rows,
            "totalCount": total_count
        }

    finally:
        conn.close()


# --------------------------
# Non-SELECT query helpers
# --------------------------

def insert_query(sql: str, params: tuple = ()):
    if not sql.strip().lower().startswith("insert"):
        raise ValueError("Only INSERT queries are allowed")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        # Ambil last inserted row (kalau ada output misalnya pakai OUTPUT INSERTED.*)
        try:
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result_rows = [dict(zip(columns, r)) for r in rows]
        except Exception:
            columns, result_rows = [], []

        return {
            "message": "insert success",
            "rows": result_rows
        }

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def update_query(sql: str, params: tuple = ()):
    if not sql.strip().lower().startswith("update"):
        raise ValueError("Only UPDATE queries are allowed")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        try:
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result_rows = [dict(zip(columns, r)) for r in rows]
        except Exception:
            columns, result_rows = [], []

        return {
            "message": "update success",
            "rows": result_rows
        }

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def delete_query(sql: str, params: tuple = ()):
    if not sql.strip().lower().startswith("delete"):
        raise ValueError("Only DELETE queries are allowed")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()

        return {
            "message": "success"
        }

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
