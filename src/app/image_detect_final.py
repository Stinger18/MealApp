from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from PIL import Image
import requests
import os
import json

'''
This program runs a testing suite on combinations of uploaded images and prompts. It scans a directory for images,
uploads them to Gyazo, and then processes them with Hugging Face Llama-3.2-Vision-Instruct.

Final output is saved as:
{ "Cheese": 1, "Cauliflower": 2 }

Uploaded images are automatically deleted from Gyazo after the consolidated results are saved.
'''

# Load environment variables
load_dotenv()

# Constants
GYAZO_API_URL = "https://upload.gyazo.com/api/upload"
GYAZO_ACCESS_TOKEN = os.getenv("gyazoAccessToken")  # gyazo access token
IMAGES_DIR = "images"  # Directory containing images
TEMPERATURE = 0.1

# Prompts for the AI
prompts = [
    """Identify the most noticeable food items and quantities from this image in JSON format with no other text. 
    Only include unique, specific food items (no categories). Example:
    [
        { "item": "Orange juice", "quantity": 1 },
        { "item": "Apple", "quantity": 2 },
        { "item": "Lemons", "quantity": 3 }
    ]
    """
]

# Initialize Hugging Face client
client = InferenceClient(api_key=os.getenv("hfKey"))


def upload_to_gyazo(image_path: str) -> str:
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


def delete_from_gyazo(image_url: str):
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



def gather_image_urls_from_directory(directory: str) -> list:
    """Iterates over a directory, uploads images to Gyazo, and returns their URLs."""
    urls = []
    for filename in os.listdir(directory):
        if filename.lower().endswith((".jpg", ".png", ".jpeg", ".gif")):
            image_path = os.path.join(directory, filename)
            try:
                gyazo_url = upload_to_gyazo(image_path)
                urls.append(gyazo_url)
            except Exception as e:
                print(f"Failed to upload {filename}: {e}")
    return urls


def delete_all_images(urls: list[str]):
    """Deletes all uploaded images from Gyazo."""
    print("\nDeleting all uploaded images...")
    for url in urls:
        delete_from_gyazo(url)


def detect_ingredients(url: str, prompt: str) -> str:
    """Processes an image URL using Hugging Face API and returns the response."""
    print("\n***** Detecting Image *****\n")
    response_text = ""
    try:
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
            print(message.choices[0].delta.content, end="")  
            response_text += message.choices[0].delta.content  # Add tokens to string
        print("\n***************\n")

        # Ensure JSON completeness
        if response_text.strip().startswith("[") and response_text.strip().endswith("]"):
            return response_text.strip()
        else:
            raise ValueError("Incomplete JSON response detected.")
    except Exception as e:
        print(f"Error during detection: {e}")
        return ""  # Return an empty response to skip processing


def test_prompts(urls: list[str], prompts: list[str]):
    """Tests prompts against all image URLs and consolidates results."""
    final_results = {}  # Collect all detected ingredients here (as a dictionary)

    for prompt in prompts:
        for url in urls:
            result = test_prompt(url, prompt)
            if result:  # If detection returned valid data, append it
                for item in result:
                    # Aggregate results (summing quantities for duplicate items)
                    if item["item"] in final_results:
                        final_results[item["item"]] += item["quantity"]
                    else:
                        final_results[item["item"]] = item["quantity"]

    # Save consolidated results as a Python dictionary
    save_final_results(final_results)

    # delete all images after processing 
    delete_all_images(urls)


def test_prompt(url: str, prompt: str) -> list[dict]:
    """Processes a single URL and returns the detected ingredients as a list of dictionaries."""
    try:
        response = detect_ingredients(url, prompt)
        return json.loads(response.strip())  # Parse JSON string into Python object
    except json.JSONDecodeError as e:
        print(f"JSON parsing error for {url}: {e}")
        return []  # Skip invalid responses
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return []


def save_final_results(results: dict):
    """Saves consolidated results as a Python dictionary."""
    consolidated_file = "consolidated_results.txt"
    try:
        with open(consolidated_file, "w") as f:
            f.write(json.dumps(results, indent=4))  # Save dictionary as JSON with pretty printing
        print(f"Consolidated results saved to {consolidated_file}")
    except Exception as e:
        print(f"Error saving consolidated results: {e}")


# Main Execution
if __name__ == "__main__":
    print("Gathering image URLs from directory...")
    urls = gather_image_urls_from_directory(IMAGES_DIR)
    print("\nStarting prompt tests...")
    test_prompts(urls, prompts)
