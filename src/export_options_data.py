import sqlite3
import pandas as pd

DB_PATH = "data/solution/duplicate_questions.db"
OUTPUT_FILE = "data/solution/duplicate_option_explanations.xlsx"


def load_data():
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            duplicate_option_id,
            reference_question_id,
            duplicate_question_id,
            duplicate_question_text,
            option_index,
            option_text,
            is_correct,
            explanation_text,
            difficulty,
            created_at
        FROM duplicate_option_explanations
        ORDER BY reference_question_id, duplicate_question_id, option_index;
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


df = load_data()
df.to_excel(OUTPUT_FILE, index=False)

print(f"Exported {len(df)} rows to {OUTPUT_FILE}")
