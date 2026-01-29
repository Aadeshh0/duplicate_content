import os 
import sqlite3
import pandas as pd

db_path = 'data/solution/duplicate_questions.db'
output_file = 'data/solution/duplicate_questions.xlsx'

def load_data():
    conn = sqlite3.connect(db_path)

    query = """
            SELECT * 
            FROM duplicate_questions;
            """
    
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


df = load_data()

df.to_excel(output_file)

print(f"Exported {len(df)} rows to {output_file}")