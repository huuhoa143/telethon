from telethon.sync import TelegramClient


def con(phone, api_id, api_hash):
    client = TelegramClient(phone, api_id, api_hash)

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

    return client
