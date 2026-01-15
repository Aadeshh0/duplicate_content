import sqlite3

def init_db(path = "data/duplicate_questions.db"):
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS duplicate_questions (
        duplicate_question_id TEXT PRIMARY KEY,
        reference_question_id TEXT,
        question_text TEXT,
        final_answer TEXT,
        difficulty TEXT
    )
    """)

    conn.commit()
    return conn


def insert_records(conn, records):
    cur = conn.cursor()

    cur.executemany("""
    INSERT INTO duplicate_questions VALUES (?, ?, ?, ?, ?)
    """, [
        (
            r["duplicate_question_id"],
            r["reference_question_id"],
            r["question_text"],
            r["final_answer"],
            r["difficulty"]
        )
        for r in records
    ])

    conn.commit()