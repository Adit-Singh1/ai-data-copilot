from app.tools.sql_tool import get_zero_traffic_cells, get_all_cells_summary
from app.tools.pandas_tool import analyze_zero_traffic, analyze_traffic_trends, detect_recently_dropped

def execute_plan(state):
    results = []

    for step in state["plan"]:
        step_lower = step.lower()

        if any(word in step_lower for word in ["zero", "identify", "filter"]):
            # SQL: basic zero traffic list
            sql_data = get_zero_traffic_cells()
            if sql_data:
                formatted = "Zero traffic cells (SQL):\n"
                for row in sql_data:
                    formatted += f"  - {row[0]}: {row[1]} days with zero traffic\n"
                results.append(formatted)

            # Pandas: deeper zero traffic analysis
            df = analyze_zero_traffic()
            if not df.empty:
                formatted = "Zero traffic analysis (Pandas):\n"
                for _, row in df.iterrows():
                    formatted += f"  - {row['cell_name']}: zero for {row['zero_days']} out of 7 days\n"
                results.append(formatted)

        elif any(word in step_lower for word in ["trend", "pattern", "collect", "data", "summary"]):
            # Pandas: traffic trends
            stats = analyze_traffic_trends()
            if not stats.empty:
                formatted = "Traffic trend analysis (Pandas):\n"
                for _, row in stats.iterrows():
                    formatted += f"  - {row['cell_name']}: total={row['total']}, avg={row['avg']:.1f}, min={row['min']}, max={row['max']}\n"
                results.append(formatted)

        elif any(word in step_lower for word in ["investigate", "cause", "drop", "recent"]):
            # Pandas: detect cells that recently dropped to zero
            dropped = detect_recently_dropped()
            if dropped:
                formatted = "Cells that recently dropped to zero:\n"
                for cell in dropped:
                    formatted += f"  - {cell['cell_name']}: dropped on {cell['last_date']}, previous max was {cell['prev_max_traffic']}\n"
                results.append(formatted)
            else:
                results.append("No cells detected as recently dropped to zero.")

        else:
            results.append(f"Processed: {step.strip()}")

    return {"intermediate_results": results}
