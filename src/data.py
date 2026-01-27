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

def load_image_questions():
    df = pd.read_excel("data/image_questions.xlsx")

    print(f'Column names of OG data : {list(df.columns)}')
    
    required_cols = ['id', 'text', 'image', 'difficulty']

    filter_df = df[required_cols]
    filter_df = filter_df.rename(columns = {
                                "id" : "question_id",  
                                "text" : "question_text", 
                                "image" : "image_url"
                            })

    print(f'Column names of image questions data : {list(filter_df.columns)}')

    filter_df["image_url"] = filter_df["image_url"].where(filter_df["image_url"].notna(), None)

    return filter_df

def group_image_questions(df: pd.DataFrame) -> pd.DataFrame:
    grouped_image_df = (
        df.groupby("question_id", as_index=False)
        .agg({
            "question_text" : "first",
            "image_url" : "first",
            "difficulty" : "first"
        })
    )

    print(f"After grouping on unique question id : {len(grouped_image_df)}")

    return grouped_image_df

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

def build_image_payload(grouped_image_df: pd.DataFrame) -> list[dict]:
    payload = []

    for i, row in grouped_image_df.iterrows():
        question = {
            "text": row["question_text"],
            "difficulty": int(row["difficulty"])
        }

        if row["image_url"] is not None:
            question["image_url"] = row["image_url"]

        payload.append({
            "reference_question_id": int(row["question_id"]),
            "question": question
        })

    print(f"Total (image + non-image) questions sent: {len(payload)}")

    return payload

def load_image_urls():
    df = pd.read_excel("data/image_questions.xlsx")

    print(f'Column names of OG data : {list(df.columns)}')

    extracted_df = df[['id', 'image']]
    extracted_df = extracted_df.rename(columns = {"id" : "question_id", "image" : "image_url"})

    filter_df = (extracted_df.groupby("question_id", as_index=False)
        .agg({
            "image_url" : "first"
        }))

    print(f'Total Image URLs fetched : {len(filter_df)}')

    filter_df["image_url"] = filter_df["image_url"].where(filter_df["image_url"].notna(), None)

    return filter_df
