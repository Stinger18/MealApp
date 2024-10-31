from openai import OpenAI, Stream
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("GPT_API_KEY"))


def query_gpt_4(prompt: str) -> Stream[ChatCompletionChunk]:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user",
                   "content": [{
                       "text": "text",
                       "text": prompt
                   }]
                   }],
        stream=True
    )
    # return response.choices[0].message.content
    return response

# Check if the user query is a GPT with database query or not
def is_database_query(query: str) -> bool:
    gpt_keywords = ["new", "random", "recommend", "suggest", "find", "search", "provide", "create", "discover"]
    if any(keyword in query.lower() for keyword in gpt_keywords):
        return False
    db_keywords = ["recipe", "recipes",
                   "ingredient", "ingredients", "meal plan"]
    return any(keyword in query.lower() for keyword in db_keywords)


user_query = "I want recipes with chicken"
use_db = is_database_query(user_query)

response = None
if use_db:
    print("Using database")
    # db_query = extract_query_params(user_query)
    # db_data = get_data_from_db(db_query)
    # print(db_data)
else:
    print("Using GPT-4")
    # response = query_gpt_4(user_query)

if response:
    for chunk in response:
        print(chunk.choices[0].delta.content or "", end="")
