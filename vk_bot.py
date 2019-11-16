import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import bs4

class VkBot:

    def __init__(self, user_id):
        print("Создан объект бота!")
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ВРЕМЯ", "ПОКА"]

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

token = "11a6e50ceacffd27faefb555ce9a1db946fc5f79b5d7d22b9571337392dae6c8265a595286eac59f484c7"

vk = vk_api.VkApi(token=token)

def write_msg(user_id, random_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random_id})


longpoll = VkLongPoll(vk)

# # Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:

            # Сообщение от пользователя
            request = event.text

            # Каменная логика ответа
            if request == "привет":
                write_msg(event.user_id, event.random_id, f"xай")
                print("dfgdf")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")

