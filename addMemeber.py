from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputPeerChannel
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
import csv
import sys
import random
import traceback
import time

api_id = 3326729
api_hash = 'a7e07f018cba287a7c6641d06836cd18'
phone = '+84961782317'

client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

input_file = sys.argv[1]
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)


chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.id == 558770466:
            groups.append(chat)
    except:
        continue

print('Choose a group to add members:')

i = 0
for g in groups:
    print(str(i) + '- ' + g.title)
    i += 1

g_index = input('Enter a Number of Group: ')
target_group = groups[int(g_index)]

print(target_group.migrated_to)
target_group_entity = InputPeerChannel(target_group.migrated_to.channel_id,target_group.migrated_to.access_hash)

print(target_group_entity)
mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

if mode == 1:
    user_to_add = InputPeerUser(user['id'], user['access_hash'])
elif mode == 2:
    user_to_add = client.get_input_entity(user['username'])
else:
    sys.exit("Invalid Mode Selected. Please Try Again.")

n=0
for user in users:
    n += 1
    if n % 50 == 0:
        time.sleep(1800)
    try:
        print('Adding {} '.format(user['id']))
        if mode == 1:
            if user['username'] == '':
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("Waiting 60 second .....")
        time.sleep(60)
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue
