import pandas as pd
import sqlite3

DB_PATH = "data/sample.db"

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM cells", conn)
    conn.close()
    df['date'] = pd.to_datetime(df['date'])
    return df

def analyze_zero_traffic():
    df = load_data()

    # Filter last 7 days
    last_7 = df[df['date'] >= pd.Timestamp.now() - pd.Timedelta(days=7)]

    # Zero traffic cells
    zero_cells = last_7[last_7['traffic'] == 0]

    # Days each cell had zero traffic
    zero_summary = zero_cells.groupby('cell_name').size().reset_index()
    zero_summary.columns = ['cell_name', 'zero_days']
    zero_summary = zero_summary.sort_values('zero_days', ascending=False)

    return zero_summary

def analyze_traffic_trends():
    df = load_data()

    last_7 = df[df['date'] >= pd.Timestamp.now() - pd.Timedelta(days=7)]

    # Traffic stats per cell
    stats = last_7.groupby('cell_name')['traffic'].agg([
        'sum', 'mean', 'min', 'max', 'std'
    ]).reset_index()

    stats.columns = ['cell_name', 'total', 'avg', 'min', 'max', 'std']
    stats = stats.sort_values('total', ascending=True)

    return stats

def detect_recently_dropped():
    df = load_data()
    df = df.sort_values(['cell_name', 'date'])

    results = []

    for cell, group in df.groupby('cell_name'):
        group = group.sort_values('date')
        traffic_list = group['traffic'].tolist()
        date_list = group['date'].tolist()

        # Check if cell had traffic before but now has zero
        if len(traffic_list) >= 2:
            had_traffic_before = any(t > 0 for t in traffic_list[:-1])
            currently_zero = traffic_list[-1] == 0

            if had_traffic_before and currently_zero:
                results.append({
                    'cell_name': cell,
                    'last_date': str(date_list[-1].date()),
                    'last_traffic': traffic_list[-1],
                    'prev_max_traffic': max(traffic_list[:-1])
                })

    return results
