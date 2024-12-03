from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from PIL import Image
import requests
import os 
import json


''' 
This Program runs a testing suite on combinations of uploaded images and prompts. It scans a directory for images, 
uploads them to Gyazo, and then processes them with Hugging Face Llama-3.2-Vision-Instruct.

NOTE:
You need a Gyazo access token and a Hugging Face API key.

Final output is saved as:
{item: qty}
'''

# Load environment variables
load_dotenv()

# Constants
GYAZO_API_URL = "https://upload.gyazo.com/api/upload"
GYAZO_ACCESS_TOKEN = os.getenv("gyazoAccessToken")  # Your Gyazo access token
IMAGES_DIR = "images"  # Directory containing images
TEMPERATURE = 0.1

# Prompts for the AI
prompts = [
    """ Identify the most noticeable food items and quantities from this image in JSON format with no other text. 
        Only identify items you are sure of. EX: 
[{
    "Orange juice": 1,
    "Apple": 2,
    "Lemons": 3
}]
"""
]

# Initialize Hugging Face client
client = InferenceClient(api_key=os.getenv("hfKey"))

def __upload_to_gyazo(image_path: str) -> str:
    """Uploads an image to Gyazo and returns the public URL."""
    print(f"Uploading {image_path} to Gyazo...")
    with open(image_path, "rb") as img_file:
        response = requests.post(
            GYAZO_API_URL,
            headers={"Authorization": f"Bearer {GYAZO_ACCESS_TOKEN}"},
            files={"imagedata": img_file}
        )
        response.raise_for_status()  # Raise an error for HTTP failures
        gyazo_url = response.json()["url"]
        print(f"Uploaded to Gyazo: {gyazo_url}")
        return gyazo_url

def __delete_from_gyazo(image_url: str):
    """Deletes an image from Gyazo using its image ID and logs detailed response."""
    try:
        #get id from url
        image_id = image_url.split("/")[-1].split(".")[0]
        delete_url = f"https://api.gyazo.com/api/images/{image_id}"

        #send DELETE request so it doesnt get in your captures and you can re-run the code with no errors
        response = requests.delete(
            delete_url,
            headers={"Authorization": f"Bearer {GYAZO_ACCESS_TOKEN}"}
        )
        
        if response.status_code == 204:
            print(f"Successfully deleted image: {image_url}")
        elif response.status_code == 200:
            print(f"Possible successful deletion with status 200 for image: {image_url}")
        else:
            print(f"Failed to delete image: {image_url}, Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")  # Log the response body for debugging
    except Exception as e:
        print(f"Error deleting image {image_url}: {e}")

def __delete_all_images(urls: list[str]):
    """Deletes all uploaded images from Gyazo."""
    print("\nDeleting all uploaded images...")
    for url in urls:
        __delete_from_gyazo(url)

def __gather_image_urls_from_directory(directory: str) -> list:
    """Iterates over a directory, uploads images to Gyazo, and returns their URLs."""
    urls = []
    for filename in os.listdir(directory):
        if filename.lower().endswith((".jpg", ".png", ".jpeg", ".gif")):
            image_path = os.path.join(directory, filename)
            try:
                gyazo_url = __upload_to_gyazo(image_path)
                urls.append(gyazo_url)
            except Exception as e:
                print(f"Failed to upload {filename}: {e}")
    return urls


def __detect_ingredients(url: str, prompt: str, outputToConsole: bool) -> str:
    """Processes an image URL using Hugging Face API and returns the response."""
    if (outputToConsole): print("\n***** Model Detecting Image *****\n")
    response_text = ""
    for message in client.chat_completion(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": url}},
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
            max_tokens=1000,
            stream=True,
            temperature=TEMPERATURE
    ):  
        if (outputToConsole): print(message.choices[0].delta.content, end="")  # Print to console
        response_text += message.choices[0].delta.content  # Add tokens to string
    if (outputToConsole): print("\n***************\n")
    return response_text


def __test_prompts(urls: list[str], prompts: list[str]):
    """Tests prompts against all image URLs."""
    try:
        os.mkdir("test_results")
    except FileExistsError:
        pass  # Directory already exists

    cnt = 0
    for prompt in prompts:
        for url in urls:
            __test_prompt(url, prompt, cnt)
            cnt += 1


def __test_prompt(url: str, prompt: str, num: int):
    """Processes a single URL and saves the results."""
    # Create result file
    result_file = f"test_results/{num}.txt"
    try:
        prediction = __detect_ingredients(url, prompt, True)
        with open(result_file, "w") as f:
            f.write(f"\n****************** {num}.txt ***********************\n")
            f.write(f"~~~ Prompt:\n\n{prompt}\n")
            f.write(f"~~~ URL:\n\n{url}\n")
            f.write(f"\n~~~ Temperature: {TEMPERATURE}\n")
            #Find out if prompt resulted in parsable response
            try:
                __to_python_dict(prediction)
                f.write("~~~ JSON to python dict parsable: PASS")
            except:
                f.write("~~~ JSON to python dict parsable: FAIL")
            f.write("\n\"\"\"\n")
            f.write(prediction)
            f.write("\n\"\"\"\n")
    except Exception as e:
        print(f"Error writing results for {url}: {e}")

    # Save image locally for reference
    try:
        img_data = requests.get(url).content
        with open(f"test_results/{num}.jpg", "wb") as img_file:
            img_file.write(img_data)
    except Exception as e:
        print(f"Error saving image from {url}: {e}")

def __to_python_dict(prediction: str):
    """Converts the json output into a python dict"""
    dict = {}
    try:
        dict = (json.loads(prediction)[0])
    except:
        print("Error: converting image prediction text into dict failed")        
    return dict
    
def __add_dict(d1: dict, d2: dict):
    """Adds all pairs from d2 to d1. If they have the same key the values are added (assummed as numbers)"""
    for key, value in d2.items():
        if key in d1:
            d1[key] += value  
        else:
            d1[key] = value  
    return d1

#Method inteded for outside users
def get_ingredients(imagesDirectory: str):
    """Detects image contents and returns a python dict (combines results from all files in imagesDirectory)"""

    print("Gathering image URLs from directory...")
    urls = __gather_image_urls_from_directory(imagesDirectory)
    print("Detecting ingredients...")

    #Add results of all pictures into one dict
    prediction = {}
    for url in urls:
        result = __to_python_dict(__detect_ingredients(url, prompts[0], True) )
        prediction = __add_dict(prediction, result)

    #Delete all images from gyazo to prevent erros
    # __delete_all_images(urls)
    return json.dumps(prediction, indent=4) #convert to json obj before returning

print(get_ingredients("desktop/workspace/whats-for-dinner/src/app/images"))