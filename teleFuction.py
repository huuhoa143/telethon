from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.tl.functions.channels import InviteToChannelRequest, GetFullChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserChannelsTooMuchError, UserBannedInChannelError, UserBlockedError, UserKickedError
import csv
import sys
import traceback
import time
import os
from datetime import datetime

from decouple import config


# api_id = int(config('API_ID'))
# api_hash = config('API_HASH')
# phone = config('PHONE')
#
# client = TelegramClient(phone, api_id, api_hash)
#
# client.connect()
# if not client.is_user_authorized():
#     client.send_code_request(phone)
#     client.sign_in(phone, input('Enter the code: '))


def get_data(client):
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
        print(str(i) + '- ' + str(g) + '\n')
        i += 1

    g_index = input('Enter a Number of Group: ')
    return groups[int(g_index)]


def get_main_group(groups):
    print('Choose a group to add members to: ')

    i = 0
    for g in groups:
        print(str(i) + '- ' + str(g) + '\n')
        i += 1

    g_index = input('Enter a Number of Group: ')
    return groups[int(g_index)]


def fetching_member(client, path_file, target_group):
    print('Fetching Members .....')
    all_participants = client.get_participants(target_group, aggressive=True)

    print('Saving in file .....')
    with open(path_file, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
        for user in all_participants:
            accept = True
            try:
                lastDate = user.status.was_online
                num_months = (datetime.now().year - lastDate.year) * 12 + (datetime.now().month - lastDate.month)
                if (num_months > 1):
                    accept= True
            except:
                continue

            if accept:
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


def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)


def get_member_running(path_file):
    users = []
    if not os.path.exists(path_file):
        print("Create File")
        open(path_file, 'w', encoding='UTF-8')
    else:
        with open(path_file, encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=",", lineterminator="\n")
            for row in rows:
                if row:
                    users.append(row[0])
    return users


def get_channel_info(client, channel_entity):
    channel_full_info = client(GetFullChannelRequest(channel=channel_entity))
    return channel_full_info


def add_member(client, input_file, target_group):
    users = []
    running_member_file = 'member_running_{}.csv'.format(target_group.id)

    member_running = get_member_running(running_member_file)

    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {'username': row[0], 'id': int(row[1]), 'access_hash': int(row[2]), 'name': row[3]}
            users.append(user)

    if hasattr(target_group, 'migrated_to'):
        channel_id = target_group.migrated_to.channel_id
        channel_access_hash = target_group.migrated_to.access_hash
    else:
        channel_id = target_group.id
        channel_access_hash = target_group.access_hash

    target_group_entity = InputPeerChannel(channel_id, channel_access_hash)

    n = 0
    for user in users:
        n += 1
        if hasattr(user, 'id'):
            check = user['id']
        else:
            check = user['username']

        if check in member_running:
            print('Member Added {} '.format(check))
            continue
        else:
            try:
                print('Adding {} '.format(user['id']))
                if user['username']:
                    user_to_add = InputPeerUser(user['id'], user['access_hash'])

                    print(target_group_entity, user_to_add)
                    result = client(InviteToChannelRequest(target_group_entity, [user_to_add]))

                    if not result.updates:
                        print("Add Fail")
                    else:
                        print("Add Success")

                    if hasattr(user, 'id'):
                        content = user['id']
                    else:
                        content = user['username']

                    channel_info = get_channel_info(client, target_group)

                    total_member = channel_info.full_chat.participants_count

                    print('Total Member: {} '.format(total_member))

                    append_new_line(running_member_file, content)

                    print("Waiting 20 second .....")
                    time.sleep(20)
                else:
                    print("NOT USER NAME")
                    continue
            except PeerFloodError:
                print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
                break
            except UserPrivacyRestrictedError:
                print("The user's privacy settings do not allow you to do this. Skipping.")
            except UserChannelsTooMuchError:
                print("One of the users you tried to add is already in too many channels/supergroups. Skipping.")
            except UserBannedInChannelError:
                print("You're banned from sending messages in supergroups/channels.. Skipping.")
            except UserBlockedError:
                print("User blocked. Skipping.")
            except UserKickedError:
                print("This user was kicked from this supergroup/channel.")
            except:
                traceback.print_exc()
                print("Unexpected Error")
                continue
