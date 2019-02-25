
# file = 'lab2/hkbaptistu/hkbaptistu.json'

# with open(file, 'r') as f:
#     for line in f.readlines():
#         print(line.strip())
import json
with open('lab2/example.json', 'r') as f:
    x = json.load(f)
    for item in x:
        print(item)
        if item['caption'] is not None:
                print('created_time: % s' % item['caption']['created_time'])
                print('Caption: % s' % item['caption']['text'])
