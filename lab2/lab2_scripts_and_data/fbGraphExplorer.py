# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 23:21:25 2019
"""


import facebook

graph = facebook.GraphAPI(access_token='EAAENboflqucBAFcP68Sz7KifpeWYZBN83gmpSEbqNeZChRFYkomeCUiZAubqMOsh9y6VqDX32IiTYMZBjhnzREUewURK6w4Ya9wA8NR3LCaeuWZBAeBwZCGQyABfuRSOAzJC5sXCQo6bG71TclGEyZA6MfOULAX4dpMHUwR9eU3hW754ePm1xLtrJ8kohJtPDpHfvZA2wWpXPgZDZD')
post = graph.get_object('me/posts')
# print(post)

msgs = [msg['message'] for msg in post['data'] if msg.get('message')]
print('Messages:')
for msg in msgs:
    # encode('utf-8') to read the emoji
    print(msg.encode('utf-8'))

storys = [msg['story'] for msg in post['data'] if msg.get('story')]
print('Story:')
for story in storys:
    # encode('utf-8') to read the emoji
    print(story.encode('utf-8'))

like = graph.get_object('me/likes')
print('Pages Liked:')
print(like)

friend = graph.get_object('me/friends')
print('Friends:')
print(friend)
