# This is a sample Python script.
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from config import token, group_token, min_age, max_age
from message import send_message, get_save_result
from search import username, user_search, get_foto_user

vk = vk_api.VkApi(token=group_token)
longpoll = VkLongPoll(vk)
token = token


def counter(offset):
    offset = offset + 2
    return offset


key_start = VkKeyboard(one_time=True)
key_start.add_button("начать", color=VkKeyboardColor.POSITIVE)
keyboard = VkKeyboard()
keyboard.add_button("вперед", color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button("закончить", color=VkKeyboardColor.POSITIVE)
key_next = VkKeyboard()
key_next.add_button("вперед", color=VkKeyboardColor.PRIMARY)
key_next.add_line()
key_next.add_button("закончить", color=VkKeyboardColor.POSITIVE)
index = 0
check = 0
check_prev = 0
user_name = ""
user_sex = ""
user_city_title = ""
user_birthday = ""
user_relation = ""
user_city_id = ""
save_result = []


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text
        if index == 0:
            user_name, user_sex, user_city_title, user_birthday, user_relation, user_city_id = username(event.user_id)
            index = 1

        match request:
            case "привет":
                offset = 0
                if check == 0:
                    send_message(event.user_id, "Для начала поиска нажмите кнопку: начать", attachment=None,
                             keyboard=key_start)
                else:
                    send_message(event.user_id, "!!! Иначе !!!", attachment=None,
                             keyboard=key_start)
            case "начать":
                offset = 0
                if user_birthday == "None":
                    send_message(event.user_id, "Введите год рождения")
                else:
                    sex = "женщин" if user_sex == 1 else "мужчин"
                    send_message(event.user_id, "Отлично, начали", keyboard=keyboard)
                    send_message(event.user_id, f"Ищем в г.{user_city_title},  {sex} ,  {user_birthday} года рождения", None,
                             keyboard=keyboard)
                    result_users_search = user_search(user_sex, user_birthday, user_city_id, user_relation,
                                                      event.user_id)  
                    output = len(result_users_search)  
                    three_most_liked, partners_id = get_foto_user(result_users_search[offset])  # вывод результата поиска фотографий

                    if not three_most_liked:  # если вывод фото пустой то ищем следующего
                        offset = counter(offset)
                        try:
                            three_most_liked.remove(result_users_search[offset])
                        except ValueError:
                            three_most_liked, partners_id = get_foto_user(result_users_search[offset])

                    send_message(event.user_id, f"Вот что я нашел : vk.com/id{partners_id} ", three_most_liked, keyboard=None)
                    save_result.append(partners_id)
                    result_users_search.insert(offset + 1, False)
                    save_result.append(False)
            case "избранное":
                save_result.pop()
                save_result.append(True)
            case "вперед":
                offset = counter(offset)
                try:
                    three_most_liked, partners_id = get_foto_user(result_users_search[offset])
                except IndexError:
                    send_message(event.user_id, "Больше ничего нет", keyboard=keyboard)
                if not three_most_liked:
                    result_users_search.remove(result_users_search[offset])
                    three_most_liked, partners_id = get_foto_user(result_users_search[offset])

                send_message(event.user_id, f"Вот что я нашел : vk.com/id{partners_id} ", three_most_liked, keyboard=key_next)
                result_users_search.insert(offset + 1, True)
                save_result.append(partners_id)
                save_result.append(False)

            case "закончить":
                index = 0
                send_message(event.user_id, "До свидания", keyboard=key_start)
                get_save_result(event.user_id, save_result)
                save_result.clear()
            case "назад":
                check_prev = 1
                if check_prev == 1:
                    send_message(event.user_id, "Достигнуто начало просмотра.", keyboard=keyboard)

            case _:
                if len(request) == 4:
                    try:
                        int(request)
                        if int(min_age) <= int(request) <= int(max_age):
                            send_message(event.user_id, "Отлично, давайте начнем!", keyboard=key_start)
                            user_birthday = request
                        else:
                            send_message(event.user_id, "Введите еще раз")
                    except ValueError:
                        send_message(event.user_id, "непонятная команда")
                else:
                    send_message(event.user_id, "Приветствую !!!")

if __name__ == 'main':
    pass
