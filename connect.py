from telethon.sync import TelegramClient
from decouple import config

api_id = int(config('API_ID'))
api_hash = config('API_HASH')
phone = config('PHONE')

def con():
    client = TelegramClient(phone, api_id, api_hash)

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))


    return client
