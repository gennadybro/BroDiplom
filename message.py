import vk_api
from random import randrange
from DataBase.database import add_parthers_data
from config import token, group_token

# vk_me = vk_api.VkApi(token=token, api_version='5.131').get_api()
vk = vk_api.VkApi(token=group_token)


def send_message(user_id, message, attachment=None, keyboard=None):
    post = {'user_id': user_id,
            'message': message,
            'random_id': randrange(10 ** 7)
            }
    if attachment is not None:
        attach = ''
        for res in attachment:   
            attach += str(res)
            attach += ','
            post['attachment'] = attach
    if keyboard is not None:
        post['keyboard'] = keyboard.get_keyboard()
    else:
        post = post
    vk.method('messages.send', post)


def get_save_result(user_id, search_result):
    print(f"save search_result: {search_result}")
    i = 0
    while i < len(search_result):
        partners = search_result[i]
        favorites = search_result[i + 1]
        print(i, partners, favorites)
        add_parthers_data(user_id, partners, favorites)
        i += 2




