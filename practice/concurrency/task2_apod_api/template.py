from api_key import key
import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor

API_KEY = key()
APOD_ENDPOINT = "https://api.nasa.gov/planetary/apod"
OUTPUT_IMAGES = "./output_images"


def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    response = requests.get(
        f"{APOD_ENDPOINT}?api_key={api_key}&start_date={start_date}&end_date={end_date}"
    )
    return json.loads(response.content)


def download_image(day: dict):
    img = requests.get(day["url"])
    with open(f"{OUTPUT_IMAGES}/{day['date']}.jpg", "wb") as f:
        f.write(img.content)


def download_apod_images(metadata: list):
    with ThreadPoolExecutor() as executor:
        executor.map(
            download_image, (day for day in metadata if day["media_type"] == "image")
        )


def main():
    metadata = get_apod_metadata(
        start_date="2021-08-01",
        end_date="2021-09-30",
        api_key=API_KEY,
    )
    print(metadata)
    download_apod_images(metadata=metadata)


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_IMAGES):
        os.makedirs(OUTPUT_IMAGES)
    main()
