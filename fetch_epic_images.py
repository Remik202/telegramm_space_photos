import argparse
import os
from datetime import datetime
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

from image_downloader import download_image


def get_epic_links(api_key, max_images):
    endpoint = 'https://api.nasa.gov/EPIC/api/natural'
    params = {'api_key': api_key}
    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    image_records = response.json()
    links = []

    for record in image_records[:max_images]:
        date = datetime.strptime(record['date'], '%Y-%m-%d %H:%M:%S')
        name = record['image']
        base_url = f'https://api.nasa.gov/EPIC/archive/natural/{date:%Y/%m/%d}/png/{name}.png'
        full_url = f'{base_url}?{urlencode({"api_key": api_key})}'
        links.append((full_url, name))

    return links


def download_epic_images(links):
    for index, (link, _) in enumerate(links, start=1):
        filename = f'epic{index}.png'
        filepath = os.path.join('space_gallery', filename)
        download_image(link, filepath)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description='Скачивает изображения Земли с NASA EPIC'
    )
    parser.add_argument('--api-key', default=os.getenv('NASA_API_KEY'), help='API-ключ NASA')
    parser.add_argument('--count', type=int, default=5, help='Количество изображений (по умолчанию 5)')
    args = parser.parse_args()

    if not args.api_key:
        raise RuntimeError('NASA_API_KEY не найден в .env и не передан через --api-key')

    links = get_epic_links(args.api_key, args.count)
    download_epic_images(links)


if __name__ == '__main__':
    main()