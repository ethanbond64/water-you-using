import os
import base64
import json
import requests

from dotenv import load_dotenv

SYTEM_PROMPT = """
You are an AI chatbot tasked with helping consumers make informed decisions about products with respect to their environmental impact, specifically water usage. 
You have been trained on a dataset of product/food information and environmental impact data.

Users will upload images of the INGREDIENTS LIST of a product, and you will provide information on the water usage of the product.
YOU WILL TAKE THE TOP 10 INGREDIENTS FROM THE INGREDIENTS LIST ONLY. FOR EACH INGREDIENT, YOU WILL PROVIDE A SENTENCE ON ITS WATER USAGE.
FINALLY, YOU WILL PROVIDE A SCORE OUT OF 100 FOR THE PRODUCT WHERE 0 IS THE WORST WATER USAGE AND 100 IS THE MOST SUSTAINABLE WATER USAGE.

The format of your response should be EXCLUSIVELY A SINGLE JSON OBJECT with the following format:
{
    "<ingredient1 by name>": "<sentence on water usage of ingredient1>",
    "<ingredient2 by name>": "<sentence on water usage of ingredient2>",
    ...
    "score": <score out of 100>
}
"""

USER_PROMPT = """
I have uploaded the image of my product, please provide the water information for the product in the appropriate JSON format.
"""

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_path):
    base64_image = encode_image(image_path)

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": SYTEM_PROMPT
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": USER_PROMPT
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
        "max_tokens": 4096
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", 
                            headers={ "Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}, 
                            json=payload)
    
    content = response.json()['choices'][0]['message']['content']
    json_info = content.replace("```json", "").replace("```", "")
    
    return json.loads(json_info)