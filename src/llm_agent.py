import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv('GEMINI_API_KEY'),
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

def call_llm_agent():
    system_prompt = """
                        You are a data augmentation system.

                        Rules:
                        - Generate semantically equivalent duplicate questions.
                        - Do NOT change meaning.
                        - Do NOT change the correct answer.
                        - Difficulty remains identical.
                        - Output ONLY valid JSON.
                        - No explanations.
                    """
    
    user_prompt = """
                    Input:
                    {input_json}

                    Output JSON schema:
                    {
                    "results": [
                        {
                        "reference_question_id": "<original id>",
                        "duplicates": [
                            {
                            "question_text": "<new paraphrased question>",
                            "final_answer": "<same as original>",
                            "difficulty": "<same as original>"
                            }
                        ]
                        }
                    ]
                    }
                """
    
    response = client.chat.completions.create(
        model = 'gemini-2.5-flash',
        messages = [
            {'role' : 'system', 'content' : system_prompt},
            {'role' : 'user', 'content' : json.dumps(user_prompt)}
        ],
        response_format={"type": "json_object"}
    )

    