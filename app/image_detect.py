
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
'''
What I think would be great for this file is to just have a class (or just function?)
that takes in an image and spits out every ingredient in a list it thinks are in the image. 
(Maybe the function also takes in a confidence interval?)

output as nested lists
[[ingredient, amount], [ingredient, amount]]
or
[[ingredient1, ingredient2...], [amount1, amount2...]]
'''

'''
Netlify website I made with bunch of test images
https://stalwart-blancmange-7f715f.netlify.app/

all images are found at
url/pic1.png
url/pic2.png
etc...
'''
urls = [
        'https://stalwart-blancmange-7f715f.netlify.app/pic1.png',
        'https://stalwart-blancmange-7f715f.netlify.app/pic2.png',
        'https://stalwart-blancmange-7f715f.netlify.app/pic3.png',
        'https://stalwart-blancmange-7f715f.netlify.app/pic4.png',
        'https://stalwart-blancmange-7f715f.netlify.app/pic5.png',
        'https://stalwart-blancmange-7f715f.netlify.app/pic6.png',
        'https://stalwart-blancmange-7f715f.netlify.app/pic7.png',
        'https://stalwart-blancmange-7f715f.netlify.app/pic8.png',
        'https://stalwart-blancmange-7f715f.netlify.app/pic9.png',
        'https://stalwart-blancmange-7f715f.netlify.app/pic10.png'
        ]

prompts = [
        'Identify the food items and quantity froms this image and return in a python dict.'
        ]

#This is for using the .env file from Ethan if you have it
load_dotenv()

#if you want to run you need an api key and permission to use meta-llama/Llama-3.2-11B-Vision-Instruct from hugging face
#if you don't want to sign up ask me or ethan to send you one 
client = InferenceClient(api_key="API_KEY_GOES_HERE")


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

def test_prompts(urls: list, prompts: str):
    print("***** Testing Prompts *****")
    for url in urls:
        detect_ingredients(url, prompts[0])

test_prompts(urls, prompts)
    
