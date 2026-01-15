from data import load_filtered_data, group_questions, build_llm_payload
from llm_agent import call_llm_agent

df = load_filtered_data()
grouped_df = group_questions(df)
payload = build_llm_payload(grouped_df[:2])

response = call_llm_agent(payload)
# print(response)