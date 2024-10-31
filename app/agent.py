from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("GPT_API_KEY"))


def query_gpt_4(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    # return response.choices[0].message.content
    return response

# Example usage
user_query = "How can I make a recipe with chicken and pasta?"
response = query_gpt_4(user_query)
for chunk in response:
    print(chunk.choices[0].delta.content or "", end="")
