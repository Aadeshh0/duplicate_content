from data import load_filtered_data, group_questions, build_llm_payload
from llm_agent import call_llm_agent, normalize_llm_response_reason, call_llm_agent_with_reason
from db import init_db, insert_records

import time 
import json

df = load_filtered_data()
grouped_df = group_questions(df)
print(f'\n || Grouped and extracted the question ids. Total questions extracted : {len(grouped_df)} ||')

for i, row in grouped_df.iterrows():
    reference_question = {
        "reference_question_id" : int(row["question_id"]),
        "question": {
            "text": row["question_text"],
            "difficulty": int(row["difficulty"])
        }
    }

    llm_response = call_llm_agent_with_reason(reference_question)

    if llm_response:
        records = normalize_llm_response_reason(llm_response)