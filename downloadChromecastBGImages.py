import os

import requests
from PIL import Image


def download_images_from_chromecastbg(url, folder):
    # Send GET request to Chromecast BG API
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return

    # Parse JSON response
    try:
        data = response.json()
    except ValueError as e:
        print(f"Failed to parse JSON response: {e}")
        return

    # Iterate over images and download them
    for image_data in data:
        image_name = f"{image_data['name']}"

        # Download image from URL
        try:
            img_response = requests.get(image_data["url"])
            if img_response.status_code != 200:
                print(f"Failed to retrieve {image_name}. Status code: {img_response.status_code}")
                continue
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {image_name}: {e}")
            continue

        # Save image to disk
        try:
            with open(folder + '/' + image_name, 'wb') as f:
                f.write(img_response.content)
        except OSError as e:
            print(f"Failed to save {image_name}: {e}")

# Usage
url = "https://chromecastbg.alexmeub.com/images.v9.json"
folder = 'chromecastBackgrounds'
os.makedirs(folder, exist_ok=True)
download_images_from_chromecastbg(url, folder)
