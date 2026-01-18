import sqlite3

def init_db(path = "data/duplicate_questions.db"):
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS duplicate_questions (
        duplicate_question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        reference_question_id INTEGER NOT NULL,
        question_text TEXT NOT NULL,
        options TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        difficulty INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    return conn


def insert_records(conn, records):
    cur = conn.cursor()

    cur.executemany("""
    INSERT INTO duplicate_questions (
        reference_question_id,
        question_text,
        options,
        correct_answer,
        difficulty
    )
    VALUES (?, ?, ?, ?, ?)
    """, [
        (
            r["reference_question_id"],
            r["question_text"],
            r["options"],
            r["correct_answer"],
            r["difficulty"]
        )
        for r in records
    ])

    conn.commit()
