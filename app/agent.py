from huggingface_hub import InferenceClient
import requests

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-11B-Vision-Instruct"
headers = {"Authorization": "Bearer hf_***"}


client = InferenceClient(api_key="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")

image_url = "https://cdn.britannica.com/61/93061-050-99147DCE/Statue-of-Liberty-Island-New-York-Bay.jpg"

for message in client.chat_completion(
        model="meta-llama/Llama-3.2-11B-Vision-Instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {
                        "url": image_url}},
                    {"type": "text",
                     "text": "Describe this image in one sentence."},
                ],
            }
        ],
        max_tokens=500,
        stream=True,
):
    print(message.choices[0].delta.content, end="")
