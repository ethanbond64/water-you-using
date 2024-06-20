# import os

# from openai import OpenAI

# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# # Function to use OpenAI to extract text
# def extract_text_from_image(image_bytes):
#     response = client.Image.create_variation(
#         image=image_bytes,
#         prompt="Extract the ingredients list from this image",
#         n=1,
#         size="1024x1024"
#     )
#     return response['choices'][0]['text']

# # Extract text from the image
# extracted_text = extract_text_from_image()
# print("Extracted Text:", extracted_text)
import os
import base64
import requests

from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key
api_key = os.environ.get("OPENAI_API_KEY")

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "static/imgs/text.png"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What’s in this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())