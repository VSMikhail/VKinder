import requests
from random import randint
import datetime
# from datetime import timedelta
from tokens import vk_chat_bot_token, vk_user_token
from pprint import pprint


class Vk:
    def __init__(self, token: str):
        self.token = token

    def get_name(self, user_id: int) -> str:
        """Функция возвращает имя и фамилию пользователя ВК в именительном падеже."""
        if user_id:
            param = {'user_ids': user_id, 'v': '5.131', 'access_token': self.token}
            r = requests.get('https://api.vk.com/method/users.get', params=param).json()
            user_name = r['response'][0]['first_name'] + ' ' + r['response'][0]['last_name']
        else:
            print('Пользователь не доступен')
            user_name = None
        return user_name

    def get_birthdate(self, user_id: int) -> datetime:
        """Функция возвращает дату рождения пользователя ВК, если она доступна в полном формате.
          В остальных случаях возвращает значение None."""
        birthdate = None
        if user_id:
            param = {'user_ids': user_id, 'v': '5.131', 'access_token': self.token, 'fields': 'bdate'}
            r = requests.get('https://api.vk.com/method/users.get', params=param).json()
            try:
                birthdate_str = r['response'][0]['bdate']
                if len(birthdate_str) > 5:
                    birthdate = datetime.datetime.strptime(birthdate_str, '%d.%m.%Y')
                else:
                    birthdate = None
            except KeyError:
                birthdate = None
        return birthdate

    def get_age_delta(self, user_id_1: int, user_id_2: int) -> int:
        """Функция возвращает модуль разницы возрастов в днях."""
        if user_id_2 and user_id_1:
            age_delta = abs(self.get_birthdate(user_id_1) - self.get_birthdate(user_id_2)).days
        else:
            age_delta = None
        return age_delta

    def check_user(self, user_id: int) -> int:
        """Проверка ID пользователя ВК на доступность. Принтует в консоль всю информацию.
        Возвращает ID -> int либо None в зависимости от результата проверки"""
        id = None
        param = {'user_ids': user_id, 'v': '5.131', 'access_token': self.token, 'fields': ['deactivated', 'is_closed']}
        r = requests.get('https://api.vk.com/method/users.get', params=param).json()
        user = r['response']

        if bool(user):
            print('Пользователь существует')
            if not user[0].get('deactivated'):
                print('Пользователь не заблокирован')
                if not user[0].get('can_access_closed'):
                    print('Пользователь не доступен')
                else:
                    print('Пользователь доступен')
                    id = user_id
            else:
                print('Пользователь заблокирован')
        else:
            print('Пользователь не существует')
        return id


inst_vk = Vk(vk_user_token)
random_number = randint(0, 50000000)
# print(random_number)
print(inst_vk.get_birthdate(21330854))
print(inst_vk.get_birthdate(10098151))
print(inst_vk.get_age_delta(21330854, 10098151))
# print(inst_vk.get_name(inst_vk.check_user(random_number)), inst_vk.check_user(random_number)) 21330854 10098151









