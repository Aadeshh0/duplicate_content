from data import load_filtered_data, group_questions, build_llm_payload
from llm_agent import normalize_llm_response_with_reason, call_llm_agent_with_reason
from db import init_db, insert_option_explanation

import time 
import json

df = load_filtered_data()
grouped_df = group_questions(df)
print(f'\n || Grouped and extracted the question ids. Total questions extracted : {len(grouped_df)} ||\n')

for idx, row in grouped_df.iterrows():
    reference_question = {
        "reference_question_id" : int(row["question_id"]),
        "question": {
            "text": row["question_text"],
            "difficulty": int(row["difficulty"])
        }
    }

    print(f" -- #{idx} STARTING LLM CALL -- ")
    llm_response = call_llm_agent_with_reason(reference_question, idx)
    print(" -- LLM RESPONSE RECEIVED -- ")
    # print('-'*25)
    print(f"Reference questions : {reference_question}")
    print(f'\n Type check for LLM Resposne : {type(llm_response)}')
    # print(f"\n LLM Response : \n {llm_response}")
    # print('-'*25)

    print(" ----- CALLING NORMALIZE FUNCTION HERE ----- ")
    records = normalize_llm_response_with_reason(
                            llm_response= llm_response,
                            ref_question_id=reference_question["reference_question_id"],
                            difficulty=reference_question["question"]["difficulty"], 
                            idx=idx
                            )
    print(" ----- ENDING NORMALIZE FUNCTION HERE ----- ")
    print(f" \n -- Type of records after normalization : {type(records)} -- \n")
    print(f"\nTotal records ready for DB insert: {len(records)}")

    conn = init_db()
    print("Connection initialized, created the duplication options table if not already there!")
    print("INSERTING Records into the DB Table")
    print(f"Inserting {len(records)} rows into the table.") 
    insert_option_explanation(conn, records=records)
    print(" -- Insertion complete! -- ")
    conn.close()





    # need to connect this normalize function's output to the db insert function 
    # make sure the is_correct is converted into binary (1, 0) from str (true, false)
    # print out the response from normalize and check its type list[dict]


    # if llm_response:
    #     records = normalize_llm_response_reason(llm_response)