import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from models import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///bot.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
token_list = ['123']


def ml_part(query_string):
    return "blablabla"


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
    main()
