import os
import time
import random
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError


def main():
    load_dotenv()

    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    post_interval = float(os.getenv('POST_INTERVAL_HOURS', 4)) * 3600

    if not bot_token or not chat_id:
        raise RuntimeError('Не указан TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID')

    bot = Bot(token=bot_token)
    photo_dir = 'space_gallery'

    while True:
        photos = [file for file in os.listdir(photo_dir) if file.lower().endswith(('.jpg', '.png'))]

        if not photos:
            print('В папке нет фотографий.')
            break

        random.shuffle(photos)

        for filename in photos:
            photo_path = os.path.join(photo_dir, filename)

            try:
                with open(photo_path, 'rb') as photo:
                    photo_bytes = photo.read()

                bot.send_photo(chat_id=chat_id, photo=photo_bytes)
                print(f'Отправлено: {filename}')
            except TelegramError as error:
                print(f'Ошибка при отправке {filename}: {error}')

            time.sleep(post_interval)


if __name__ == '__main__':
    main()