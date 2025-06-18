import os
import argparse
import requests
from dotenv import load_dotenv

from image_downloader import download_image, extract_file_extension


def get_apod_images(api_key, count):
    nasa_apod_api = 'https://api.nasa.gov/planetary/apod'
    params = {'count': count, 'api_key': api_key}
    response = requests.get(nasa_apod_api, params=params)
    response.raise_for_status()
    return response.json()


def download_apod_images(images):
    for index, image in enumerate(images, start=1):
        if image.get('media_type') != 'image':
            continue

        link = image['url']
        ext = extract_file_extension(link)
        filename = f'nasa{index}{ext}'
        filepath = os.path.join('space_gallery', filename)

        download_image(link, filepath)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description='Скачивает изображения с NASA APOD (Astronomy Picture of the Day)'
    )
    parser.add_argument('--api-key', default=os.getenv('NASA_API_KEY'), help='API-ключ NASA')
    parser.add_argument('--count', type=int, default=5, help='Количество изображений (по умолчанию 5)')
    args = parser.parse_args()

    if not args.api_key:
        raise RuntimeError('NASA API ключ не указан и не найден в .env')

    images = get_apod_images(args.api_key, args.count)
    download_apod_images(images)


if __name__ == '__main__':
    main()