from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from time import sleep
import sys
import csv
import traceback
import time
import random



# api_id = 2183869
# api_hash = ''
# phone = '+'
# client = TelegramClient(phone, api_id, api_hash)

# client.connect()
# if not client.is_user_authorized():
#     client.send_code_request(phone)
#     client.sign_in(phone, input('Enter the code: '))
    

def read_file():

    # FILE DATA
    input_file = sys.argv[1]
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[1]
            user['id'] = int(row[0])
            user['access_hash'] = int(row[3])
            user['name'] = row[4]
            users.append(user)

    # FILE TO COMPARE
    input_file_compare = sys.argv[2]
    users_compare = []
    with open(input_file_compare, encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['id'] = int(row[0])
            users_compare.append(user)
    
    return users, users_compare


def get_group(client):
    chats = []
    last_date = None
    chunk_size = 200
    groups=[]
    result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup== True:
                groups.append(chat)
        except:
            continue

    print('Choose a group to add members:')
    i=0
    for group in groups:
        print(str(i) + '- ' + group.title)
        i+=1

    g_index = input("Enter a Number: ")
    target_group=groups[int(g_index)]

    target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
    mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

    return target_group_entity, mode

def main():

    api_id = 2688800
    api_hash = ''
    phone = '+'
    client = TelegramClient(phone, api_id, api_hash)

    # DEAN
    #api_id = 
    #api_hash = ''
    #phone = '+'
    #client = TelegramClient(phone, api_id, api_hash)

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

    users, users_compare = read_file()
    target_group_entity, mode = get_group(client)

    #print(target_group_entity)

    n = 0
    for user in users:
        compare_group_1 = 0
        for user_com in users_compare:
            if int(user['id']) == int(user_com['id']):
                compare_group_1 = int(user_com['id'])
                break
        if compare_group_1 == int(user['id']):
            #print(compare_group_1)
            continue
        else:
            n += 1
            if n % 50 == 0:
                sleep(900)
            try:
                if mode == 1:
                    if user['username'] == "":
                        continue
                    #print ("Adding {}".format(user['id']))
                    user_to_add = client.get_input_entity(user['username'])
                elif mode == 2:
                    
                    user_to_add = InputPeerUser(user['id'], user['access_hash'])
                else:
                    sys.exit("Invalid Mode Selected. Please Try Again.")
                print ("Adding {}".format(user['id']))
                client(InviteToChannelRequest(target_group_entity,[user_to_add]))
                print("Waiting for 60-180 Seconds...")
                time.sleep(random.randrange(120, 180))
            except PeerFloodError:
                print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
            except UserPrivacyRestrictedError:
                print("The user's privacy settings do not allow you to do this. Skipping.")
            except:
                traceback.print_exc()
                print("Unexpected Error")
                continue


main()


# -------------------------------------------------------------------------------------------------
# api_id = 
# api_hash = ''
# phone = '+'
# client = TelegramClient(phone, api_id, api_hash)

# client.connect()
# if not client.is_user_authorized():
#     client.send_code_request(phone)
#     client.sign_in(phone, input('Enter the code: '))

# # FILE DATA
# input_file = sys.argv[1]
# users = []
# with open(input_file, encoding='UTF-8') as f:
#     rows = csv.reader(f, delimiter=",", lineterminator="\n")
#     next(rows, None)
#     for row in rows:
#         user = {}
#         user['username'] = row[1]
#         user['id'] = int(row[0])
#         user['access_hash'] = int(row[3])
#         user['name'] = row[4]
#         users.append(user)

# # FILE TO COMPARE
# input_file_compare = sys.argv[2]
# users_compare = []
# with open(input_file_compare, encoding='UTF-8') as f:
#     rows = csv.reader(f, delimiter=",", lineterminator="\n")
#     next(rows, None)
#     for row in rows:
#         user = {}
#         user['id'] = int(row[0])
#         users_compare.append(user)


# chats = []
# last_date = None
# chunk_size = 200
# groups=[]
# result = client(GetDialogsRequest(
#             offset_date=last_date,
#             offset_id=0,
#             offset_peer=InputPeerEmpty(),
#             limit=chunk_size,
#             hash = 0
#         ))
# chats.extend(result.chats)

# for chat in chats:
#     try:
#         if chat.megagroup== True:
#             groups.append(chat)
#     except:
#         continue

# print('Choose a group to add members:')
# i=0
# for group in groups:
#     print(str(i) + '- ' + group.title)
#     i+=1

# g_index = input("Enter a Number: ")
# target_group=groups[int(g_index)]

# target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
# mode = int(input("Enter 1 to add by username or 2 to add by ID: "))


# n = 0
# for user in users:
#     compare_group_1 = 0
#     for user_com in users_compare:
#         if int(user['id']) == int(user_com['id']):
#             compare_group_1 = int(user_com['id'])
#             break
#     if compare_group_1 == int(user['id']):
#         #print(compare_group_1)
#         #print(int(user['id']))
#         #sleep(50)
#         continue
#     else:
#         n += 1
#         if n % 50 == 0:
#             sleep(900)
#         try:
#             print ("Adding {}".format(user['id']))
#             if mode == 1:
#                 if user['username'] == "":
#                     continue
#                 user_to_add = client.get_input_entity(user['username'])
#             elif mode == 2:
#                 user_to_add = InputPeerUser(user['id'], user['access_hash'])
#             else:
#                 sys.exit("Invalid Mode Selected. Please Try Again.")
#             client(InviteToChannelRequest(target_group_entity,[user_to_add]))
#             print("Waiting for 60-180 Seconds...")
#             time.sleep(random.randrange(60, 180))
#         except PeerFloodError:
#             print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
#         except UserPrivacyRestrictedError:
#             print("The user's privacy settings do not allow you to do this. Skipping.")
#         except:
#             traceback.print_exc()
#             print("Unexpected Error")
#             continue
