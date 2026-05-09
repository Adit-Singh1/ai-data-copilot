import pandas as pd
import sqlite3
import os

DB_PATH = "data/sample.db"

def process_csv(file_bytes: bytes, filename: str) -> dict:
    try:
        # Read CSV into dataframe
        import io
        df = pd.read_csv(io.BytesIO(file_bytes))

        # Normalize column names to lowercase
        df.columns = [col.strip().lower() for col in df.columns]

        # Check required columns exist
        required = ['cell_name', 'traffic', 'date']
        missing = [col for col in required if col not in df.columns]

        if missing:
            return {
                "success": False,
                "error": f"Missing columns: {missing}. Required: {required}. Found: {list(df.columns)}"
            }

        # Clean data
        df['traffic'] = pd.to_numeric(df['traffic'], errors='coerce').fillna(0).astype(int)
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        df = df[['cell_name', 'traffic', 'date']].dropna()

        # Insert into database
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM cells")  # Clear old data
        conn.executemany(
            "INSERT INTO cells (cell_name, traffic, date) VALUES (?, ?, ?)",
            df[['cell_name', 'traffic', 'date']].values.tolist()
        )
        conn.commit()
        conn.close()

        return {
            "success": True,
            "rows": len(df),
            "cells": df['cell_name'].nunique(),
            "date_range": f"{df['date'].min()} to {df['date'].max()}",
            "preview": df.head(5).to_dict(orient='records')
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
