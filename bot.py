import time
import re

from telethon import TelegramClient, sync, types
import telebot

# Параметры авторизации
api_id = 
api_hash = ''
phone = ''
session_file = ''

# Создаем клиента Telegram
client = TelegramClient(session_file, api_id, api_hash)

def process_message(message, channel_username):
    if r"Открыли доступ" in message:
        print(f'Реклама "Открыли доступ" {channel_username} ')
        return None  # Возвращаем None, если сообщение содержит "Открыли доступ"
    if channel_username == "smart_signal_free":
        message = re.sub(r'http\S+', 'https://t.me/Abramov_Trade', message)  # удалить все ссылки

    if channel_username == 'marzherubs':
        message = re.sub(r'http\S+', 'https://t.me/Abramov_Trade', message)  # удалить все ссылки

    if channel_username == 'Whale_Hunter_Crypto':
        message = re.sub(r'http\S+', '', message) # удалить все ссылки
        message = message.split('Не забывайте ставить', 1)[0]
        message = message.split('Ссылка', 1)[0]

    if channel_username == "cryptobarbos":
        message = message + "\n#Отзывы"

    message = message + "\n✏️ Связь со мной: @abramov_trader"
    print(message)
    return message

# Определяем функцию для отправки сообщения в канал
def send_message_channel(message,channel_username):
    message_text = process_message(message.raw_text, channel_username)
    if message_text == None:
        return None
    bot = telebot.TeleBot('')

    # If the message contains media, send it as a photo or video
    if message.media:
        media_list = []

        if isinstance(message.media, types.MessageMediaPhoto):
            photo_data = client.download_media(message.media)
            photo = telebot.types.InputMediaPhoto(open(photo_data, 'rb'), caption=message_text)
            media_list.append(photo)
        elif isinstance(message.media, types.MessageMediaDocument):
            if not(channel_username == "Makar_Potapov") and not(channel_username == "roman_blog_crypto"): # не качать с Макара Потапова видео
                video_data = client.download_media(message.media)
                video = telebot.types.InputMediaVideo(open(video_data, 'rb'), caption=message_text)
                media_list.append(video)
        try:
            bot.send_media_group(chat_id='-1001918056588', media=media_list)
        except:
            bot.send_message(chat_id='-1001918056588', text=message_text)

    else:
        # Отправляем текстовое сообщение в канал
        bot.send_message(chat_id='-1001918056588', text=message_text)


def start_bot():
    # Авторизуем клиента
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

    # Получаем ID канала
    channel_usernames = [
        # 'troshin_official',
        'smart_signal_free',
        'YovioTrade',
        'marzherubs',
        'Makar_Potapov', # убраны видео
        'Whale_Hunter_Crypto', # убрана реклама
        'roman_blog_crypto',
        'cryptobarbos', # отзывы
    ]

    # print(channel_usernames)
    channel_entities = {}
    for channel_username in channel_usernames:
        channel_entities[channel_username] = client.get_entity(channel_username)

    # Бесконечный цикл для проверки новых сообщений
    last_message_ids = {channel_username: None for channel_username in channel_usernames}

    while True:
        for channel_username, channel_entity in channel_entities.items():
            # Получаем последнее сообщение в канале
            message = client.get_messages(channel_entity, limit=1)[0]

            # Проверяем, не получали ли мы это сообщение ранее
            if message.id != last_message_ids[channel_username]:
                # Сохраняем идентификатор нового сообщения
                last_message_ids[channel_username] = message.id

                # Отправляем сообщение в другой канал

                send_message_channel(message, channel_username)

        # Ждем 2 секунды, чтобы не нагружать серверы Telegram
        time.sleep(2)

if __name__ == "__main__":
    start_bot()

