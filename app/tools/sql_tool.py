import sqlite3

DB_PATH = "data/sample.db"

def run_sql(query):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        return f"SQL Error: {str(e)}"

def get_zero_traffic_cells():
    query = """
        SELECT cell_name, COUNT(*) as zero_days
        FROM cells
        WHERE traffic = 0
        AND date >= date('now', '-7 days')
        GROUP BY cell_name
        ORDER BY zero_days DESC
    """
    return run_sql(query)

def get_all_cells_summary():
    query = """
        SELECT cell_name, 
               SUM(traffic) as total_traffic,
               COUNT(*) as days_recorded,
               MIN(traffic) as min_traffic,
               MAX(traffic) as max_traffic
        FROM cells
        WHERE date >= date('now', '-7 days')
        GROUP BY cell_name
        ORDER BY total_traffic ASC
    """
    return run_sql(query)
