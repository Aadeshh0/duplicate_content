import sqlite3

def init_db(path = "data/solution/duplicate_questions.db"):
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS duplicate_questions (
        duplicate_question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        reference_question_id INTEGER NOT NULL,
        question_text TEXT NOT NULL,
        options TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        solution TEXT NOT NULL,
        difficulty INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS duplicate_image_questions (
    duplicate_question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference_question_id INTEGER NOT NULL,
    duplicate_question_text TEXT NOT NULL,
    duplicate_image TEXT,
    difficulty INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS duplicate_option_explanations (
    duplicate_option_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference_question_id INTEGER NOT NULL,
    duplicate_question_id TEXT NOT NULL,
    duplicate_question_text TEXT NOT NULL,
    option_index INTEGER NOT NULL,
    option_text TEXT NOT NULL,
    is_correct INTEGER NOT NULL,
    explanation_text TEXT NOT NULL,
    difficulty INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    return conn


def insert_records(conn, records):
    cur = conn.cursor()

    cur.executemany("""
        INSERT INTO duplicate_option_explanations (
            reference_question_id,
            duplicate_question_id,
            duplicate_question_text,
            option_index,
            option_text,
            is_correct,
            explanation_text,
            difficulty
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            r["reference_question_id"],
            r["duplicate_question_id"],
            r["duplicate_question_text"],
            r["option_index"],
            r["option_text"],
            r["is_correct"],        
            r["explanation_text"],
            r["difficulty"]
        )
        for r in records
    ])

    conn.commit()

def insert_option_explanation(conn, records):
    cur = conn.cursor()

    cur.executemany("""
    INSERT INTO duplicate_option_explanations (
        reference_question_id,
        duplicate_question_id,
        duplicate_question_text,
        option_index,
        option_text,
        is_correct,
        explanation_text,
        difficulty
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            r["reference_question_id"],
            r["duplicate_question_id"],
            r["duplicate_question_text"],
            r["option_index"],
            r["option_text"],
            r["is_correct"],  # normalize here
            r["explanation_text"],
            r["difficulty"]
        )
        for r in records
    ])

    conn.commit()

def insert_image_records(conn, records):
    cur = conn.cursor()

    cur.executemany("""
    INSERT INTO duplicate_image_questions (
        reference_question_id,
        duplicate_question_text,
        duplicate_image,
        difficulty
    )
    VALUES (?, ?, ?, ?)
    """, [
        (
            r["reference_question_id"],
            r["duplicate_question_text"],
            r["duplicate_image"],
            r["difficulty"]
        )
        for r in records
    ])

    conn.commit()


