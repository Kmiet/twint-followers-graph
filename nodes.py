
from os import listdir
import json
import time 

total_set = set()

mentions_set = set()

start = '['
end = ']'

for p in range(0, 12):
     datContent = [i for i in open("./Mentions/mentions{}_user_timeline.txt".format(p)).readlines()]
     for i in datContent:
        mentions_set.add(i.split(":")[0][3:-1])
        for j in i.split(":")[1].split(','):
             mentions_set.add(j[j.find(start)+len(start):j.rfind(end)])


print('mentions', len(mentions_set))

# for j in range(0, 12):
follows_set = set()

for p in range(0, 8):

    datContent = [i for i in open("./Follows/follows{}.dat".format(p)).readlines()]

    for i in datContent:
        k = i.split(',')
        for j in k:
            if len(j.split()) > 1:
                follows_set.add(j.split()[0])
                if j.split()[1][1] == '''"''':
                    follows_set.add(j.split()[1][2:-1])

            else:
                follows_set.add(j.split()[0][1:-1])

print('follows:', len(follows_set))

user_names = set()

for i in user_names:
    print(i)

user_names = set()

for j in range(0, 12):

    datContent = [i for i in open("./Users/users{}.dat".format(j)).readlines()]

    for i in datContent:
        res = json.loads(i)
        user_names.add(res['username'])
    
print('users:', len(user_names))

total_set.update(follows_set)
print('total:',len(total_set))

total_set.update(mentions_set)
print('total:',len(total_set))



