import os
import argparse
import requests

from image_downloader import download_image


def fetch_spacex_images(launch_id):
    url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(url)
    response.raise_for_status()

    launch = response.json()
    photo_links = launch['links']['flickr']['original']

    for index, link in enumerate(photo_links, start=1):
        filename = f'spacex{index}.jpg'
        filepath = os.path.join('space_gallery', filename)
        download_image(link, filepath)


def main():
    parser = argparse.ArgumentParser(
        description='Скачивает изображения запуска SpaceX по ID или фиксированному запуску'
    )
    parser.add_argument(
        '--launch-id',
        default='5eb87d47ffd86e000604b38a',
        help='ID запуска (по умолчанию: 5eb87d47ffd86e000604b38a)'
    )
    args = parser.parse_args()

    fetch_spacex_images(args.launch_id)


if __name__ == '__main__':
    main()