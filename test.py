import os
import csv

path_file = 'member_running_1156988081.csv'
users = []

if not os.path.exists(path_file):
    print("Create File")
    open(path_file, 'w', encoding='UTF-8')
else:
    print("Run")
    with open(path_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        for row in rows:
            if row:
                print(row[0])
                users.append(row[0])

print(users)