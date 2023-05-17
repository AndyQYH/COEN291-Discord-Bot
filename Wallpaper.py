from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import random
import numpy as np
import os
import requests
import base64
import cv2
from dotenv import load_dotenv

load_dotenv()

def get_img_from_stability(quote):
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
                    "text": quote
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

def get_wallpaper(quote, image_path = ''):
    # image_width
    get_img_from_stability(quote)
    rand1 = random.randint(5,255)
    rand2 = random.randint(5,255)
    rand3 = random.randint(5,255)
    image = Image.open(image_path + '/' + "imageToSave.png")
    image_array = np.array(image, dtype=np.uint8)
    print(image_array.shape)
    image.putalpha(128)
    image = image.filter(ImageFilter.GaussianBlur(2))
    font = ImageFont.truetype("Quicksand/static/Quicksand-Bold.ttf", 36)
    text1 = quote
    text_color = (rand1,rand2,rand3)
    text_start_height = 50
    draw_text_on_image(image, image_array, text1, font, text_color, text_start_height)
    if image_path != '':
        image.save(image_path + '/' + 'created_image.png')
    else:
        image.save('created_image.png')

def draw_text_on_image(image, image_arr, text, font, text_color, text_start_height):
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=35)
    for line in lines:
        #print(type(line))
        line_width, line_height = font.getsize(line)
        if len(lines) * line_height >= image_height:
            font.size = np.floor(image_height /  len(lines))
            line_width, line_height = font.getsize(line)
        pixels = image_arr[y_text:y_text+line_height][:]
        print(type(pixels))
        print(pixels.shape)
        draw.text(((image_width - line_width) / 2, y_text),line, font=font, fill=text_color)
        y_text += line_height
        