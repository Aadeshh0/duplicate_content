import pandas as pd

def load_filtered_data():

    df = pd.read_excel("data/master_questions.xlsx", sheet_name="Sheet1")

    print(f'Column names of OG data : {list(df.columns)}')
    
    required_cols = ['id', 'text', 'answer', 'difficulty', 'text.1']

    filter_df = df[required_cols]
    filter_df = filter_df.rename(columns = {
                                "id" : "question_id",  
                                "text" : "question_text", 
                                "answer" : "final_answer", 
                                "difficulty" : "difficulty",
                                "text.1" : "options_text"
                            })

    print(f'Column names of filtered data : {list(filter_df.columns)}')

    return filter_df

def group_questions(df: pd.DataFrame) -> pd.DataFrame:
    grouped_df = (
        df
        .groupby("question_id", as_index=False)
        .agg({
            "question_text": "first",
            "difficulty": "first"
        })
    )

    return grouped_df

def build_llm_payload(grouped_df: pd.DataFrame) -> list[dict]:
    payload = []

    for i, row in grouped_df.iterrows():
        payload.append({
            "reference_question_id": row["question_id"],
            "question": {
                "text": row["question_text"],
                "difficulty": int(row["difficulty"])
            }
        })

    return payload
