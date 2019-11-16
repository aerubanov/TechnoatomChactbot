import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from models import Base, User, Log
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import threading
import socket
from time import sleep
import requests
import bs4
from bot import Bot

engine = create_engine('sqlite:///bot.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
token_list = ['123']
req_count = 0
sock = socket.socket()
sock.connect(('35.204.44.141', 2003))
token = "11a6e50ceacffd27faefb555ce9a1db946fc5f79b5d7d22b9571337392dae6c8265a595286eac59f484c7"
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
ml = Bot()


class VkBot:

    def __init__(self, user_id):
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

    @staticmethod
    def _clean_all_tag_from_str(string_line):
        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result


def ml_part(query_string):
    if query_string[0] == '/':
        query_string = query_string[1:]
        res = ml.find_compl(query_string, 5)
        return res
    if query_string[0] == '?':
        query_string = query_string[1:]
        res = ml.find_str(query_string)
        return res
    if query_string[0] == '!':
        query_string = query_string[1:]
        res = ml.find_in_subcategpry(query_string)
        return res
    res = ml.find_similar(query_string, 5)
    return res


def agregate():
    global req_count
    sleep(60)
    sock.send(f'hackathon.team3.backend.cnt {req_count} -1\n'.encode('utf-8'))
    print('sended')
    req_count = 0


def write_msg(user_id, random_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random_id})


# # Основной цикл
def main():
    for event in longpoll.listen():

        # Если пришло новое сообщение
        if event.type == VkEventType.MESSAGE_NEW:

            # Если оно имеет метку для меня( то есть бота)
            if event.to_me:
                global req_count
                req_count = req_count + 1

                # Каменная логика ответа
                if session.query(User).filter(User.user_id == event.user_id).first():
                    row = Log(user_id=event.user_id, text=event.text)
                    session.add(row)
                    session.commit()
                    try:
                        result = ml_part(event.text)
                        #s = f'similar {result[0]}, comlimentar {result[1]}'
                        s = '\n'.join(result)
                        write_msg(event.user_id, event.random_id, s)
                    except (KeyError, TypeError) as e:
                        print(e)
                elif event.text in token_list:
                    user = User(user_id=event.user_id)
                    session.add(user)
                    session.commit()
                    write_msg(event.user_id, event.random_id,
                              f'{VkBot(event.user_id)._USERNAME}, теперь ты авторизован! Для того чтобы '
                              f'найти похожии, просто введи id. Чтобы найти комплиментарные напиши /id id'
                              f'чтобы найти по названию введди ?слово.'
                              # f' Чтобы вернуть товары из смежной категориинапиши !id'
                              )
                else:
                    write_msg(event.user_id, event.random_id,
                              f'Привет {VkBot(event.user_id)._USERNAME}! У тебя нет доступа, пришли мне токен')


if __name__ == '__main__':
    t = threading.Thread(target=agregate)
    t.start()
    main()
