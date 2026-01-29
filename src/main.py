from data import load_filtered_data, group_questions, build_llm_payload
from llm_agent import call_llm_agent, normalize_llm_response
from db import init_db, insert_records

from data import load_image_questions, group_image_questions, build_image_payload
from llm_agent import call_image_llm_agent, normalize_image_llm_response
from db import insert_image_records

import time
import json

df = load_filtered_data()
grouped_df = group_questions(df)
print(f'\n || Grouped and extracted the question ids. Total questions extracted : {len(grouped_df)} ||')

print(f'\n || [Building PAYLOAD] ||')
payload = build_llm_payload(grouped_df)
print(f'\n Payload built')

print(f'\n Calling LLM API')
startTime = time.time()
raw_response = call_llm_agent(payload)
endTime = time.time()
print(f'\n Collecting response from LLM')

timeTaken = endTime - startTime
print(f'\n || Total time taken for the llm call : {timeTaken} || ')

llm_response = json.loads(raw_response)
print('\n Normalzing llm resposne')

records = normalize_llm_response(llm_response)

print(f"\nTotal records ready for DB insert: {len(records)}")

conn = init_db()
insert_records(conn, records)
conn.close()

print("=" * 60)
print("=" * 60)
print("Image Pipeline")
print("-" * 30)

# df = load_image_questions()

# grouped_image_df = group_image_questions(df)

# image_payload = build_image_payload(grouped_image_df)

# raw_response = call_image_llm_agent(image_payload)
# llm_response = json.loads(raw_response)

# records = normalize_image_llm_response(llm_response)

# print(f"Total duplicate image questions generated: {len(records)}")

# conn = init_db()
# insert_image_records(conn, records)








