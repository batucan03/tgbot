# image.py
import requests
from PIL import Image
import io
from config import UNSPLASH_API_KEY, UNSPLASH_API_URL, IMAGE_SIZE

def fetch_image(topic):
    try:
        url = f"{UNSPLASH_API_URL}?query={topic}&client_id={UNSPLASH_API_KEY}"
        response = requests.get(url)
        data = response.json()
        if not data['results']:
            return None
        image_url = data['results'][0]['urls']['regular']
        image_response = requests.get(image_url)
        image = Image.open(io.BytesIO(image_response.content))
        if image.size != IMAGE_SIZE:
            image = image.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
        image_path = f"temp_image_{topic}.jpg"
        image.save(image_path, "JPEG")
        return image_path
    except Exception as e:
        return None
