from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

client = InferenceClient(api_key=os.getenv("HUGGINGFACE_API_KEY"))

image_url = "http://www.paleopantry.org/wp-content/uploads/2017/03/20170323-Preserving-Cooling.jpg"

for message in client.chat_completion(
        model="meta-llama/Llama-3.2-11B-Vision-Instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {
                        "url": image_url}},
                    {"type": "text",
                     "text": "Identify the food items and quantity from this image."},
                ],
            }
        ],
        max_tokens=500,
        stream=True,
):
    print(message.choices[0].delta.content, end="")
