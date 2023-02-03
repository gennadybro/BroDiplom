import vk_api
from time import sleep
from config import token
from message import send_message

from DataBase.database import open_partners_data

vk_me = vk_api.VkApi(token=token, api_version='5.131').get_api()


def username(user_id):  # сбор информации о  пользователе
    user_info = vk_me.users.get(**{'user_ids': user_id, 'fields': 'bdate, city, sex, relation'})[0]
    user_birthday = user_info.get("bdate")
    if user_birthday:
        try:
            user_birthday = int(user_birthday[-4:])
        except:
            check = 1
            send_message(user_id, f' \n К сожалению, у Вас не заполнена дата рождения,  введите год и нажмите начать')
            user_birthday = 'None'
    user_city_title = user_info.get('city', {}).get('title', None)
    user_city_id = user_info.get('city', {}).get('id', None)
    user_sex = user_info['sex']
    user_name = user_info.get('first_name')
    user_relation = user_info.get('relation')  # семейное положение
    if user_sex == 1:   # если женщина то ищем мужчину (2)
        user_sex = 2
    else:
        user_sex = 1  # если мужчина то ищем женщину (1)
    return user_name, user_sex, user_city_title, user_birthday, user_relation, user_city_id


def user_search(sex, bdate, city, relation, user_id):
    result_users_search = []

    search_result = vk_me.users.search(**{'sex': sex,
                                          'birth_year': bdate,
                                          'city': city,
                                          'fields': 'is_closed, id, first_name, last_name',
                                          'status': 1 or 6,
                                          'count': '1000'})['items']
    for result in search_result:
        if not result.get('is_closed'):
            first_name = result.get('first_name')
            last_name = result.get('last_name')
            vk_id = str(result.get('id'))
            result_users_search.append(vk_id)
        else:
            continue
    result_users_search = status(result_users_search, user_id)
    return result_users_search


def status(result_users_search, user_id):
    result_users_search_old = open_partners_data(user_id)

    i = 0
    while i < len(result_users_search_old):
        result_search = result_users_search_old[i]
        if result_search in result_users_search:
            result_users_search.remove(result_search)
        i += 1
    return result_users_search


def get_foto_user(partner_id):
    sleep(0.3)
    avatars = vk_me.photos.get(**{'owner_id': partner_id,
                                                 'album_id': 'profile',
                                                 'rev': '1',            #  берём самые свежие фото
                                                 'extended': '1',
                                                 'count': '1000'})['items']
    avatars.sort(key=lambda x: x['likes']['count'])
    avatars = avatars[-3:]
    three_most_liked = [f'photo{photo["owner_id"]}_{photo["id"]}' for photo in avatars]
    if len(three_most_liked) < 3:
        three_most_liked = []
    return three_most_liked, partner_id