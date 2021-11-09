import json

with open('json/lol-champions-v1-inventories-61663941-champions-minimal.json') as json_file:
    data = json.load(json_file)

count = 0
for champion in data:
    print(champion['name'])
    count += 1

print(count)
