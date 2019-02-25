import facebook

graph = facebook.GraphAPI(access_token='EAAf7ZCl15yJUBAK512OecstNIl4QgEuXZCVqoEHNlpcAtOZC3zhcr8pPXoSlPsKbdvtnVHkn8jLTw9HdZC1CIYpV1yJxSZAJNANCeprP0EcSLvl3C5aovHd34BggTtw1gD1ZCekOiNQseKq4bcXiSs8lzVbj4JePnknOtydlSHJmnFOrxsxlx9AT6jt4uZBdmoMVo1PMuc1vDDxPAACHbq9vCrZBZCX5YOMwZD')

post = graph.get_object('me/name')

print(post)

msgs = [msg['message'] for msg in post['data'] if msg.get('message')]

for msg in msgs:
    print(msg)
    # You can also add encode('utf-8') to read the emoji
    # print(msg.encode('utf-8'))
