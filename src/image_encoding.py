from data import load_image_urls
import base64
import requests

def encode_images_to_base64(df):
    encoded_images = []

    for i, row in df.iterrows():
        question_id = int(row["question_id"])
        url = row["image_url"]

        if not url:
            continue
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            image_bytes = response.content
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")

            encoded_images.append({
                "question_id": question_id,
                # "image_url": url,
                "image_base64": image_b64
            })

            print(f'\nEncoded image with qeustion id : {question_id}')
            print(f'[Base64 string] Encoded string : {image_b64[:120]}')

        except Exception as e:
            print(f'[FAIL] Failed for question id : {question_id}  | {e}')

    print(f'\nTotal encoded image = {len(encoded_images)}\n')

    return encoded_images

