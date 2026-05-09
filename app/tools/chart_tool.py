import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend (no GUI popup)
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import io
import base64

DB_PATH = "data/sample.db"

def get_df():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM cells", conn)
    conn.close()
    df['date'] = pd.to_datetime(df['date'])
    return df

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight',
                facecolor='#0f1117', edgecolor='none', dpi=120)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_base64

def chart_traffic_over_time():
    df = get_df()
    df = df.sort_values('date')

    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#0f1117')
    ax.set_facecolor('#1a1d27')

    colors = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
    for i, (cell, group) in enumerate(df.groupby('cell_name')):
        ax.plot(group['date'], group['traffic'],
                marker='o', label=cell,
                color=colors[i % len(colors)], linewidth=2, markersize=4)

    ax.set_title('Traffic Over Time (Last 7 Days)',
                 color='#e0e0e0', fontsize=13, pad=12)
    ax.set_xlabel('Date', color='#6b7280', fontsize=10)
    ax.set_ylabel('Traffic', color='#6b7280', fontsize=10)
    ax.tick_params(colors='#6b7280')
    ax.legend(facecolor='#1a1d27', labelcolor='#e0e0e0', fontsize=9)
    ax.grid(True, color='#2a2d3a', linestyle='--', alpha=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor('#2a2d3a')

    return fig_to_base64(fig)

def chart_zero_traffic_cells():
    df = get_df()
    last_7 = df[df['date'] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
    zero = last_7[last_7['traffic'] == 0].groupby('cell_name').size()

    if zero.empty:
        return None

    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor('#0f1117')
    ax.set_facecolor('#1a1d27')

    colors = ['#ef4444' if v == 7 else '#f59e0b' if v >= 3 else '#6366f1'
              for v in zero.values]
    bars = ax.bar(zero.index, zero.values, color=colors, width=0.5)

    ax.set_title('Zero Traffic Days per Cell (Last 7 Days)',
                 color='#e0e0e0', fontsize=13, pad=12)
    ax.set_xlabel('Cell Name', color='#6b7280', fontsize=10)
    ax.set_ylabel('Days with Zero Traffic', color='#6b7280', fontsize=10)
    ax.tick_params(colors='#6b7280')
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.grid(True, axis='y', color='#2a2d3a', linestyle='--', alpha=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor('#2a2d3a')

    for bar, val in zip(bars, zero.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                str(val), ha='center', color='#e0e0e0', fontsize=10)

    return fig_to_base64(fig)

def chart_cell_comparison():
    df = get_df()
    last_7 = df[df['date'] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
    summary = last_7.groupby('cell_name')['traffic'].mean().sort_values()

    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor('#0f1117')
    ax.set_facecolor('#1a1d27')

    colors = ['#ef4444' if v == 0 else '#10b981' if v > 100 else '#f59e0b'
              for v in summary.values]
    bars = ax.barh(summary.index, summary.values, color=colors, height=0.5)

    ax.set_title('Average Traffic per Cell (Last 7 Days)',
                 color='#e0e0e0', fontsize=13, pad=12)
    ax.set_xlabel('Average Traffic', color='#6b7280', fontsize=10)
    ax.tick_params(colors='#6b7280')
    ax.grid(True, axis='x', color='#2a2d3a', linestyle='--', alpha=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor('#2a2d3a')

    for bar, val in zip(bars, summary.values):
        ax.text(val + 1, bar.get_y() + bar.get_height()/2,
                f'{val:.0f}', va='center', color='#e0e0e0', fontsize=9)

    return fig_to_base64(fig)
