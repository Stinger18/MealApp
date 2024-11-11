
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
''' 
USAGE
if you want to run you need a hugging face key and permission to use meta-llama/Llama-3.2-11B-Vision-Instruct from hugging face
if you don't want to sign up ask james or ethan to send you one 

What I think would be great for this file is to just have a class (or just function?)
that takes in an image and spits out every ingredient in a list it thinks are in the image. 
(Maybe the function also takes in a confidence interval?)

output as nested lists
[[ingredient, amount], [ingredient, amount]]
or
[[ingredient1, ingredient2...], [amount1, amount2...]]


'''

urls = [
        'https://s1.qwant.com/thumbr/474x653/1/8/0badc5abb0852264a2cb394dd9c6a57fd451384393e62b94fb77480a054013/th.jpg?u=https://tse.mm.bing.net/th?id%3DOIP.XKV1IuS9-G5POEfJhsLfewHaKN%26pid%3DApi&q=0&b=1&p=0&a=0',
        'https://s1.qwant.com/thumbr/474x316/2/b/6227a4c72e9145fbb6a2307f162e4c68d55852c7e372a00707f6f6e0d28538/th.jpg?u=https://tse.mm.bing.net/th?id%3DOIP.GU6SQ77Cyb7DBMcvu9j6KgHaE8%26pid%3DApi&q=0&b=1&p=0&a=0',
        'https://s1.qwant.com/thumbr/474x316/9/6/d72896c72955e1ae2291077d29d97818bf997a63428f8e10ac0f275150d626/th.jpg?u=https://tse.mm.bing.net/th?id%3DOIP.h_GjdVuPrZ89d4lOTlWBfAHaE8%26pid%3DApi&q=0&b=1&p=0&a=0',
        'https://s1.qwant.com/thumbr/474x675/0/9/5fc821586b0b8cc9b2f6e8be20ea8936e9fa77f3da80e9ee33d1585ab3f441/th.jpg?u=https://tse3.explicit.bing.net/th?id%3DOIP.5gA4kIfw9vNxyKkCgE2D8QHaKj%26pid%3DApi&q=0&b=1&p=0&a=0',
        'https://s2.qwant.com/thumbr/474x684/5/5/26f1fb9dcb52c2b90518496c9421645f6041ebad64773fd6c9a08524e657f4/th.jpg?u=https://tse.mm.bing.net/th?id%3DOIP.o2tNBjbfk60KrYA00oP_XwHaKs%26pid%3DApi&q=0&b=1&p=0&a=0',
        'https://s2.qwant.com/thumbr/474x711/6/d/4045f69b7f9ccac2ec0abf1cf999dd4da797051741435d6f18547f7cd49d36/th.jpg?u=https://tse.mm.bing.net/th?id%3DOIP.Y85UVva4QJ_9ENgIsMBKnAHaLH%26pid%3DApi&q=0&b=1&p=0&a=0',
        'https://s2.qwant.com/thumbr/474x386/d/5/4cf501973975f75101dc4861cb70b73a979fd3d4e66d3ce517ea9a37a72ede/th.jpg?u=https://tse.mm.bing.net/th?id%3DOIP.GVK-YnAcS0QC-ESITx3F-wHaGC%26pid%3DApi&q=0&b=1&p=0&a=0',
        'https://s1.qwant.com/thumbr/474x500/a/9/50e07b729e6273180a44bc94c1bfaec329aef3f6097efacc0edfe81b0cf5a8/th.jpg?u=https://tse.mm.bing.net/th?id%3DOIP.2oD8uxGIpiAQlCTGgdBCcwHaH0%26pid%3DApi&q=0&b=1&p=0&a=0',
        'https://s1.qwant.com/thumbr/474x710/3/4/be8c2baa1de6beac3e6e5f880f532b5aff716f9ce904d0b5d3f8c0b525ac59/th.jpg?u=https://tse.mm.bing.net/th?id%3DOIP.-XtKmAjjhJbDwq5y1UyHaQHaLG%26pid%3DApi&q=0&b=1&p=0&a=0',
        'https://s2.qwant.com/thumbr/474x760/c/d/f08f2f2516c8fa9c238318f1b13722eab8ef93abd23331f04818d5924405a0/th.jpg?u=https://tse.mm.bing.net/th?id%3DOIP._Sc1ybWIZaV-DYW0A__iewHaL4%26pid%3DApi&q=0&b=1&p=0&a=0'
        ]

prompts = [
        'Identify the food items and quantities froms this'
        ]


# load_dotenv()
# client = InferenceClient(api_key=os.getenv("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"))

client = InferenceClient(api_key="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")

# This uses the hugging face api to access llama3.2. Also loads image from url 
def detect_ingredients(image_url: str, prompt: str):
    response_text = ""

    for message in client.chat_completion(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {
                            "url": image_url}},
                        {"type": "text",
                        "text": prompt},
                    ],
                }
            ],
            max_tokens=500,
            stream=True,
    ):
        print(message.choices[0].delta.content, end="") #prints directly to console

    #This code helps you return a string instead of printing
    #     response_text += message.choices[0].delta.content #add new tokens to string
    # return response_text


#-----Testing functions-----

def test_prompts(urls: list[str], prompts: list[str]):
    print("***** Testing Prompts *****")
    for prompt in prompts:
        for url in urls:
            test_prompt(url, prompt)

def test_prompt(url: str, prompt: str):
    print("\n******************************************\n")
    print("URL: ", url, "\n")
    print("Prompt: ", prompt)
    print("\n\"")
    detect_ingredients(url, prompt)
    print("\n\"\n")

# test_prompts(urls, prompts)
test_prompt(urls[0], prompts[0])
    
