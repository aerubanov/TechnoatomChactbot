import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from models import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import threading
import socket
from time import sleep

engine = create_engine('sqlite:///bot.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
token_list = ['123']
req_count = 0
sock = socket.socket()
sock.connect(('35.204.44.141', 2003))


def ml_part(query_string):
    return "blablabla"


def agregate():
    global req_count
    sleep(60)
    sock.send(f'hackathon.team3.backend.cnt {req_count} -1\n'.encode('utf-8'))
    print('sended')
    req_count = 0


token = "11a6e50ceacffd27faefb555ce9a1db946fc5f79b5d7d22b9571337392dae6c8265a595286eac59f484c7"

vk = vk_api.VkApi(token=token)


def write_msg(user_id, random_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random_id})


longpoll = VkLongPoll(vk)


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
                    result = ml_part(event.text)
                    write_msg(event.user_id, event.random_id, result)
                elif event.text in token_list:
                    user = User(user_id=event.user_id)
                    session.add(user)
                    session.commit()
                    write_msg(event.user_id, event.random_id, 'Теперь ты авторизован!')
                else:
                    write_msg(event.user_id, event.random_id, 'Привет! Я тебя не знаю, пришли мне токен')


if __name__ == '__main__':
    t = threading.Thread(target=agregate)
    t.start()
    main()
