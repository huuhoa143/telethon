import teleFuction
from decouple import config
import connect


# megagroup: is a group chat that have large member
# broadcast: is a channel
# ChatForbidden: only have id and title
# Check Chat or Channel own: creator=True,

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


def main():

    api_id = int(config('API_ID'))
    api_hash = config('API_HASH')
    phone = config('PHONE')

    client = connect.con(phone, api_id, api_hash)
    data = teleFuction.get_data(client)

    # list_owner_group = get_owner_group(data)

    # main_group = teleFuction.get_main_group(list_owner_group)
    main_group = client.get_entity('https://t.me/joinchat/nk7OjRbItjphMzA9')

    print(main_group)
    list_mega_group = get_mega_group(data)

    target_group = teleFuction.get_target_group(list_mega_group)

    path_file = 'memeber_{}.csv'.format(target_group.id)

    print(path_file)

    teleFuction.fetching_member(client, path_file, target_group)

    teleFuction.add_member(client, path_file, main_group)


main()
