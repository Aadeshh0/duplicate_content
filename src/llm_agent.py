import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv('GEMINI_API_KEY'),
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

def call_llm_agent(payload : list[dict]):
    system_prompt = """
                        You are a question generation system.

                        Rules:
                        - Generate 5 NEW questions.
                        - The new question must test the SAME SKILL and SAME DIFFICULTY LEVEL.
                        - The correct answer DOES NOT need to match the original.
                        - Do NOT reuse numbers, entities, or structure exactly.
                        - Output ONLY valid JSON.
                        - No explanations.

                        Clarification:
                        Paraphrasing is NOT allowed.
                        Example:
                        Original: 23 + 45 = ?
                        Valid new question: 67 + 18 = ?
                        Invalid: What is 45 plus 23? OR 63 - 21 
                    """
    
    user_prompt = f"""
                    Input:
                    {json.dumps(payload, ensure_ascii=False)}

                    Output JSON schema:
                    {{
                        "results": [
                            {{
                            "reference_question_id": "<original id>",
                            "duplicates": [
                                {{
                                "question_text": "<new paraphrased question>",
                                "difficulty": "<same as original>"
                                }}
                            ]
                            }}
                        ]
                    }}
                """
    
    print("=" * 60)
    print(f"Total questions in payload: {len(payload)}\n")

    for index, item in enumerate(payload, start=1):
        print(f"[{index}] Sending Question")
        print(f"    Reference ID : {item['reference_question_id']}")
        print(f"    Difficulty   : {item['question']['difficulty']}")
        print(f"    Text         : {item['question']['text']}\n")
        print("-" * 30)

    response = client.chat.completions.create(
        model = 'gemini-2.5-flash',
        messages = [
            {'role' : 'system', 'content' : system_prompt},
            {'role' : 'user', 'content' : user_prompt}
        ],
        response_format={"type": "json_object"}
    )

    llm_output = response.choices[0].message.content

    print('*' * 80)
    print("\n========== LLM RESPONSE RECEIVED ==========")
    print(llm_output)
    print('*' * 80)

    return llm_output