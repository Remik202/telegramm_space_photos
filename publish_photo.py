import os
import random
from dotenv import load_dotenv
from telegram import Bot


def main():
    load_dotenv()

    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not bot_token or not chat_id:
        raise RuntimeError('Не указан TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID')

    bot = Bot(token=bot_token)

    photo_dir = 'space_gallery'
    photos = [file for file in os.listdir(photo_dir) if file.lower().endswith(('.jpg', '.png'))]

    if not photos:
        raise FileNotFoundError('Нет доступных изображений в папке space_gallery')

    random_photo = random.choice(photos)
    photo_path = os.path.join(photo_dir, random_photo)

    with open(photo_path, 'rb') as photo:
        bot.send_photo(chat_id=chat_id, photo=photo)


if __name__ == '__main__':
    main()