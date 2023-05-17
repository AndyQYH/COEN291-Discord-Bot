import os
import requests
from dotenv import load_dotenv
import base64

load_dotenv()

api_host = os.getenv('API_HOST', 'https://api.stability.ai')
url = f"{api_host}/v1/engines/list"

api_key = os.getenv("STABILITY_API_KEY")
if api_key is None:
    raise Exception("Missing Stability API key.")

response = requests.get(url, headers={
    "Authorization": f"Bearer {api_key}"
})

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

# Do something with the payload...
payload = response.json()

print(payload)

engine_id = "stable-diffusion-xl-beta-v2-2-2"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = os.getenv("STABILITY_API_KEY")

if api_key is None:
    raise Exception("Missing Stability API key.")

response = requests.post(
    f"{api_host}/v1/generation/{engine_id}/text-to-image",
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    },
    json={
        "text_prompts": [
            {
                "text": "Create a visually engaging artwork that captures the concept of a group of chess players gathering in a minefield to discuss their victories, symbolizing their quest to determine the ultimate 'king' of explosions. Incorporate elements of humor and anticipation into the artwork"
            }
        ],
        "cfg_scale": 35,
        "clip_guidance_preset": "FAST_BLUE",
        "sampler":"K_EULER",
        "height": 384,
        "width": 704,
        "samples": 1,
        "steps": 70,
    },
)

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

data = response.json()

img_data_str = data['artifacts'][0]['base64']
img_data = base64.b64decode(img_data_str)

with open("images/imageToSave.png", "wb") as fh:
       fh.write(img_data)