import teleFuction
from telethon.tl.functions.messages import GetHistoryRequest
from decouple import config
import connect


def main():
    api_id = int(config('API_ID'))
    api_hash = config('API_HASH')
    phone = config('PHONE')

    client = connect.con(phone, api_id, api_hash)
    channel_username = client.get_entity("https://t.me/joinchat/SoAew9pYptuMMdZh")
    for message in client.get_messages(channel_username, limit=100):
        print(message.id, ":      " ,message.message)


main()
