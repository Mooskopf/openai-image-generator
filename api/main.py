from fastapi import FastAPI
import requests
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


class ImageGenerator(BaseModel):
    prompt: str
    size: str


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/")
def read_root():
    return ("Hello World")


@app.post("/api/generate-image")
async def get_image(ImageGenerator: ImageGenerator):
    api_key = os.getenv("API_Key")
    url = 'https://api.openai.com/v1/images/generations'

    data = {
        'prompt': ImageGenerator.prompt,
        'num_images': 1,
        'size': ImageGenerator.size,
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        # The URL of the generated image
        image_url = json.loads(response.text)['data'][0]['url']
        out = {
            "success": True,
            "image": image_url
        }
        return json.dumps(out)
    except requests.exceptions.RequestException as err:
        return json.dumps({
            "success": False,
            "error": err
        })
