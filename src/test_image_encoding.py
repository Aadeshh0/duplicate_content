from data import load_image_urls
from image_encoding import encode_images_to_base64

df = load_image_urls()
encoded_images = encode_images_to_base64(df)

print(encoded_images[0].keys())

sample = encoded_images[0]

payload = [{
    "reference_question_id": sample["question_id"],
    "question": {
        "image_base64": sample["image_base64"]
    }
}]