from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
import csv
import sys
import traceback
import time
from decouple import config

api_id = int(config('API_ID'))
api_hash = config('API_HASH')
phone = config('PHONE')

client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


def get_chats():
    last_date = None
    chunk_size = 200
    chats = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))

    chats.extend(result.chats)

    return chats


def get_target_group(groups):
    print('Choose a group to scape members from: ')

    i = 0
    for g in groups:
        print(str(i) + '- ' + g.title)
        i += 1

    g_index = input('Enter a Number of Group: ')
    return groups[int(g_index)]


def fetching_member(path_file, target_group):
    print('Fetching Members .....')
    all_participants = client.get_participants(target_group, aggressive=True)

    print('Saving in file .....')
    with open(path_file, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
        for user in all_participants:
            if user.username:
                username = user.username
            else:
                username = ''
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ''
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ''
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])
    print('Members scraped successfully')


def add_member(input_file, target_group):
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {'username': row[0], 'id': int(row[1]), 'access_hash': int(row[2]), 'name': row[3]}
            users.append(user)

    target_group_entity = InputPeerChannel(target_group.migrated_to.channel_id, target_group.migrated_to.access_hash)
    print(target_group_entity)
    mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

    n = 0
    for user in users:
        n += 1
        if n % 50 == 0:
            print('Sleep 1800s')
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
            time.sleep(20)
        except PeerFloodError:
            print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this. Skipping.")
        traceback.print_exc()
        print("Unexpected Error")
        continue
