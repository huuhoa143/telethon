import teleFuction

groups = teleFuction.get_chats()

target_group = teleFuction.get_target_group(groups)

path_file = 'memeber_{}.csv'.format(target_group.id)

print(path_file)

teleFuction.fetching_member(path_file, target_group)