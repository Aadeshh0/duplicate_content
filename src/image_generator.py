import base64
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


output_dir = "data/generated_images"
os.makedirs(output_dir, exist_ok=True)

def call_image_llm_agent(payload: list[dict]):
    system_prompt = """
    You are an educational image generation system.

    Rules:
    - Generate images similar in CONCEPT, not appearance.
    - Preserve the SAME skill being tested.
    - Change numerical values, labels, colors, and layout slightly.
    - Images must be suitable for school-level exam questions.
    - Do NOT copy exact values or structure.
    """

    user_prompt = f"""
        Generate 5 different but conceptually similar images based on this description:

        '{image_caption}

        Constraints:
        - Same difficulty level
        - Same mathematical or logical skill
        - Different numeric values
        - Different visual arrangement
        """
    
    results = []

    print("="*60)
    print(f'Total items in payload : {len(payload)}\n')

    for index, item in enumerate(payload, start=1):
        ref_id = item["reference_question_id"]
        image_caption = item["image_caption"]

        print(f"[{index}] Processing image")
        print(f"    Reference ID : {ref_id}")
        print(f"    Caption      : {image_caption}")
        print("-" * 30)

        response = client.images.generate(
            model="gemini-2.5-flash-image",
            prompt=system_prompt + "\n" + user_prompt,
            n=5,
            size="1024x1024"
        ) 

        image_paths = []

        for i, img in enumerate(response.data):
            image_base64 = img.b64_json
            image_bytes = base64.b64decode(image_base64)

            path = os.path.join(
                output_dir,
                f"{ref_id}_variant_{i+1}.png"
            )

            with open(path, "wb") as f:
                f.write(image_bytes)

            image_paths.append(path)
            print(f"Saved → {path}")

        results.append({
            "reference_question_id": ref_id,
            "generated_images": image_paths
        })

    print("*" * 80)
    print("========== IMAGE GENERATION COMPLETE ==========")
    print(json.dumps(results, indent=2))
    print("*" * 80)

    return results



