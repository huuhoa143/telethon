import teleFuction
from decouple import config
import connect
import concurrent.futures
import threading

# megagroup: is a group chat that have large member
# broadcast: is a channel
# ChatForbidden: only have id and title
# Check Chat or Channel own: creator=True,

thread_local = threading.local()

def get_owner_group(data):
    owner_group = []

    for d in data:
        try:
            if d.creator == True:
                owner_group.append(d)
        except:
            continue

    return owner_group


def get_mega_group(data):
    mega_group = []

    for d in data:
        try:
            if d.megagroup == True:
                mega_group.append(d)
        except:
            continue

    return mega_group


class Account:
    def __init__(self, api_id, api_hash, phone):
        self.api_id = int(api_id)
        self.api_hash = api_hash
        self.phone = phone


def running_account(account):
    target_group_text = 'https://t.me/tamsu9'
    api_id = account.api_id
    api_hash = account.api_hash
    phone = account.phone

    client = connect.con(phone, api_id, api_hash)
    data = teleFuction.get_data(client)

    # list_owner_group = get_owner_group(data)

    # main_group = teleFuction.get_main_group(list_owner_group)
    main_group = client.get_entity('https://t.me/joinchat/nk7OjRbItjphMzA9')

    # list_mega_group = get_mega_group(data)

    target_group = client.get_entity(target_group_text)

    path_file = 'memeber_{}.csv'.format(target_group.id)

    print(path_file)

    teleFuction.fetching_member(client, path_file, target_group)

    teleFuction.add_member(client, path_file, main_group)


def main():
    list_account = [
        Account('3326729', 'a7e07f018cba287a7c6641d06836cd18', '+84961782317'),
        Account('2397524', 'de240af5379921bb24e174b4b9ffb441', '+84798820867'),
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_run = {executor.submit(running_account(account)): account for account in list_account}
        for future in concurrent.futures.as_completed(future_to_run):
            print(future)

main()
