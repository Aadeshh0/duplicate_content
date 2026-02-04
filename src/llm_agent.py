import json
import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv('GEMINI_API_KEY'),
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

def call_llm_agent(payload : list[dict]) -> str:
    system_prompt = """
                        You are a question generation system.

                        Rules:
                        - Generate 5 NEW multiple choice questions.
                        - Each question MUST include:
                            - question_text
                            - exactly 4 valid options for its question
                            - exactly 1 valid correct answer
                            - exactly 1 detailed step by step solution explanation for correct answer
                        - Solution rules:
                            - 2-3 concise lines only
                            - Each line should be a logical step
                            - Explain only the correct answer
                            - No intro, no summary, no discussion of other options
                        - New question's text should match the input question formatting for HTML.
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
                                "question_text": "<new question>",
                                "options": [
                                            "<option 1>",
                                            "<option 2>",
                                            "<option 3>",
                                            "<option 4>"
                                            ],
                                "correct_answer": "<must match one option>",
                                "solution" : "<brief explanation of correct answer>",
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

    startTime = time.perf_counter()
    response = client.chat.completions.create(
        model = 'gemini-2.5-flash',
        messages = [
            {'role' : 'system', 'content' : system_prompt},
            {'role' : 'user', 'content' : user_prompt}
        ],
        response_format={"type": "json_object"}
    )

    elapsedTime = (time.perf_counter() - startTime) * 1000
    print(f'\n [LoggingTime] LLM call took {elapsedTime:.2f} ms')

    llm_output = response.choices[0].message.content

    if not llm_output:
        return("LLM returned empty response.")

    print('*' * 80)
    print("\n========== LLM RESPONSE RECEIVED ==========")
    print(llm_output)
    print('*' * 80)

    return llm_output

def normalize_llm_response(llm_respone : dict) -> list[dict]:
    
    flattened_records = []
    results = llm_respone.get("results", [])

    print('\n ------------ NORMALIZING LLM RESPONSE ------------')
    print(f"Total reference questions: {len(results)}")

    for result in results:
        ref_id = result.get("reference_question_id")
        duplicates = result.get("duplicates", [])

        for index, duplicate in enumerate(duplicates):
            record = {
                "reference_question_id": int(ref_id),
                "question_text": duplicate.get("question_text"),
                "options": json.dumps(duplicate["options"], ensure_ascii=False),
                "correct_answer": duplicate["correct_answer"],
                "solution" : duplicate['solution'],
                "difficulty": int(duplicate.get("difficulty"))
            }

            flattened_records.append(record)

    return flattened_records


def call_image_llm_agent(payload : list[dict]):
    system_prompt = """
                        You are a question generation system.

                        Rules:
                        - Generate exactly 5 NEW questions per input question. 
                        - The new question must test the SAME SKILL and SAME DIFFICULTY LEVEL.
                        - If the input includes an image -> Generate a description for image generation.
                        - If the input does not include an image -> Do not include any image fields.
                        - Do NOT reuse numbers or entities.
                        - Output ONLY valid JSON.
                        - No explanations.
                        - Paraphrasing is NOT allowed.

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
                                "question_text": "<new question>",
                                "duplicate_image_prompt": "<only if input had image>",
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

def normalize_image_llm_response(llm_response : dict) -> list[dict]:
    records = []
    results = llm_response.get("results", [])

    print(f"Total reference questions: {len(results)}")

    for result in results:
        ref_id = int(result["reference_question_id"])

        for dup in result.get("duplicates", []):
            records.append({
                "reference_question_id": ref_id,
                "duplicate_question_text": dup["question_text"],
                "duplicate_image": dup.get("duplicate_image_prompt"),  # nullable
                "difficulty": int(dup["difficulty"])
            })

    print(f"Total duplicate questions: {len(records)}")
    return records


def call_llm_agent_with_reason(payload : dict) -> str|None:
    system_prompt = """
                        You are a question generation system.

                        Rules:
                        - Generate 5 NEW multiple choice questions.
                        - Each question MUST include:
                            - question_text
                            - exactly 4 valid options for its question
                            - exactly 1 valid correct answer
                            - explanation_text for EACH option
                        
                        Explanation rules:
                            - If is_correct = true:
                                - explanation_text is a 2 to 3 line step-by-step solution
                            - If is_correct = false:
                                - explanation_text is a misconception explaining how a learner could reach this answer
                            - No introductions, no summaries, no references to other options
                        
                        Constraints
                        - New question's text should match the input question HTML formatting.
                        - The new question must test the SAME SKILL and SAME DIFFICULTY LEVEL.
                        - The correct answer DOES NOT need to match the original.
                        - Do NOT reuse numbers, entities, or structure exactly.
                        - Output ONLY valid JSON.

                        Clarification:
                        Paraphrasing is NOT allowed.
                        Example:
                        Original: 23 + 45 = ?
                        Valid new question: 67 + 18 = ?
                        Invalid: What is 45 plus 23? OR 63 - 21 
                    """
    
    user_prompt = f"""
                    Input:
                    {json.dumps(payload["question"], ensure_ascii=False)}

                    Output JSON schema:
                    {{
                    "duplicate_questions": [
                        {
                        "duplicate_question_text": "new question string",
                        "options": [
                            {
                            "option_text": "12",
                            "is_correct": true,
                            "explanation_text": "You added 9 and 3 correctly to get 12."
                            },
                            ...
                        ]
                        }
                    ]
                    }}

                    Hard constraints:
                    - duplicate_questions array length = 5
                    - options array length = 4
                    - exactly ONE option with is_correct = true per question
                """
    
    print("=" * 60)
    print(f"Total questions in payload: {len(payload)}\n")

    print(f"\n#1 Sending Question")
    print(f"    Difficulty   : {payload['question']['difficulty']}")
    print(f"    Text         : {payload['question']['text']}\n")
    print("-" * 30)

    startTime = time.perf_counter()
    response = client.chat.completions.create(
        model = 'gemini-2.5-flash',
        messages = [
            {'role' : 'system', 'content' : system_prompt},
            {'role' : 'user', 'content' : user_prompt}
        ],
        response_format={"type": "json_object"}
    )

    elapsedTime = (time.perf_counter() - startTime) * 1000
    print(f'\n [LoggingTime] LLM call took {elapsedTime:.2f} ms')

    llm_output = response.choices[0].message.content

    if not llm_output:
        print("LLM response is empty.")
        return None

    print('*' * 80)
    print("\n========== LLM RESPONSE RECEIVED ==========")
    print(llm_output)
    print('*' * 80)

    return llm_output

def normalize_llm_response_reason(llm_respone : str, ref_question_id : int, difficulty : int) -> list[dict]:
    
    flattened_records = []
    results = llm_respone

    print('\n ------------ NORMALIZING LLM RESPONSE ------------')
    print(f"Total reference questions: {len(results)}")

    for duplicate_index, row in enumerate(results):
        question_text = row["duplicate_question_text"]
        options = row["options"]

        for option_index, option in enumerate(options):
            flattened_records.append({
                "reference_question_id" : ref_question_id,
                "duplicate_question_id" : f"{duplicate_index}",
                "option_text": option["option_text"],
                "is_correct": int(option["is_correct"]),
                "explanation_text": option["explanation_text"],
                "difficulty": difficulty
            })

    for result in results:
        ref_id = result.get("reference_question_id")
        duplicates = result.get("duplicates", [])

        for index, duplicate in enumerate(duplicates):
            record = {
                "reference_question_id": int(ref_id),
                "question_text": duplicate.get("question_text"),
                "options": json.dumps(duplicate["options"], ensure_ascii=False),
                "correct_answer": duplicate["correct_answer"],
                "solution" : duplicate['solution'],
                "difficulty": int(duplicate.get("difficulty"))
            }

            flattened_records.append(record)

    return flattened_records

