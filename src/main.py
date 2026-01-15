from data import load_filtered_data, group_questions, build_llm_payload
from llm_agent import call_llm_agent, normalize_llm_response
from db import init_db, insert_records

import json

df = load_filtered_data()
grouped_df = group_questions(df)

payload = build_llm_payload(grouped_df)

raw_response = call_llm_agent(payload)

llm_response = json.loads(raw_response)

records = normalize_llm_response(llm_response)

print(f"\nTotal records ready for DB insert: {len(records)}")

conn = init_db()
insert_records(conn, records)
