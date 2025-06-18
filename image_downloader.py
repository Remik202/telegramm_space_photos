import os
import requests
from urllib.parse import urlsplit, unquote


def download_image(image_link, target_filepath):
    os.makedirs(os.path.dirname(target_filepath), exist_ok=True)

    response = requests.get(image_link)
    response.raise_for_status()

    with open(target_filepath, 'wb') as file:
        file.write(response.content)


def extract_file_extension(image_link):
    image_path = urlsplit(image_link).path
    image_filename = os.path.basename(unquote(image_path))
    _, extension = os.path.splitext(image_filename)
    return extension