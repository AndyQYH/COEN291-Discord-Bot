from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import random
import numpy as np
import os
import requests
import base64
import colorsys
import replicate
import urllib.request
from dotenv import load_dotenv

load_dotenv()
height = 512
width =768
steps = 70
seed = 62800

def get_img_from_stability(quote, model = "stable-diffusion-xl-beta-v2-2-2"):
    engine_id =  model
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = os.getenv("STABILITY_API_KEY")
    
    print("generating from stability AI ...")

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
            "height": height,
            "width": width,
            "samples": 1,
            "steps": steps,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    img_data_str = data['artifacts'][0]['base64']
    img_data = base64.b64decode(img_data_str)

    with open("images/imageToSave.png", "wb") as fh:
        fh.write(img_data)
        
def download_image(url, file_path, file_name):
    full_path = file_path + file_name + '.png'
    urllib.request.urlretrieve(url, full_path)
        
def get_img_from_prompt_hero(quote ="hello world!", model = "prompthero/openjourney:9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb"):
    print("generating from open journey ...")
    
    if model == "prompthero/openjourney-v4:e8818682e72a8b25895c7d90e889b712b6edfc5151f145e3606f21c1e85c65bf":
        output = replicate.run(
            model_version = model,
            input={"prompt": quote, 
                    "width": width,
                    "height": height,
                    "num_inference_steps": 50,
                    "seed": seed, 
                    "guidance_scale": 20}
        )
    else:
        output = replicate.run(
        model_version = model,
        input={"prompt": quote, 
            "width": width,
            "height": height,
            "num_inference_steps": 50,
            "guidance_scale": 20}
        )
    print(output)
    return output[0]
    
def get_wallpaper(quote, prompt,  image_path = '', source = 'Stability.ai Stable Diffusion SD XL', model_stable = "stable-diffusion-xl-beta-v2-2-2", model_hero = "prompthero/openjourney:9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb"):
    # image_width
    if source == 'Stability.ai Stable Diffusion SD XL':
        get_img_from_stability(quote = prompt, model=model_stable)
    else:
        image_url = get_img_from_prompt_hero(quote = prompt, model=model_hero)
        download_image(image_url, 'images/', "imageToSave")
        
    image = Image.open(image_path + '/' + "imageToSave.png")
    image_array = np.asarray(image)
    print('Complementing...')
    lo = np.amin(image_array, axis=2, keepdims=True)
    hi = np.amax(image_array, axis= (0,1))
    print("high: \n", hi)
    #image_array_comp = (lo + hi) - image_array
    image_array_comp = 255 - image_array
    out_img = Image.fromarray(image_array_comp)
    lo_comp = np.amin(image_array_comp, axis=2, keepdims=True)
    hi_comp = np.amax(image_array_comp, axis= (0,1))
    print("high comp: \n", hi_comp)
    out_img.putalpha(255)
    image.putalpha(128)
   
    #mask = Image.new(mode ='L',size = image.size, color = 0)
    image = image.filter(ImageFilter.GaussianBlur(2))
    font = ImageFont.truetype("Quicksand/static/Quicksand-Bold.ttf", 36)
    text1 = quote
    text_color = tuple(hi_comp)
    text_start_height = 50
    draw_text_on_image(image, text1, font, text_color, text_start_height)
    #image_comp = Image.composite(out_img, image, mask)
    if image_path != '':
        out_img.save(image_path + '/' + 'created_image_2.png')
        image.save(image_path + '/' + 'created_image.png')
        #image_comp.save(image_path + '/' + 'created_image.png')
    else:
        out_img.save('created_image_2.png')
        image.save('created_image.png')
        #image_comp.save('created_image.png')
    
    
def draw_text_on_image(image, text, font, text_color, text_start_height):
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
       
        draw.text(((image_width - line_width) / 2, y_text),line, font=font, fill=text_color)
        y_text += line_height
        
        
   
#get_wallpaper(quote = "Hello World!", prompt = "an anime girl with cat ear", image_path='images')     
#image_url = get_img_from_prompt_hero(quote = "an anime girl with cat ear")
#download_image(image_url, 'images/', "imageToSave")
#get_img_from_stability(quote = "What did the German wine say when it rode a motorcycle? \"I can't handle this much horsepower!\"")