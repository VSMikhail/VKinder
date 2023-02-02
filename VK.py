import requests
import datetime


class Vk:
    def __init__(self, token: str):
        self.token = token

    def search_potential_partners(self, sex: int = 0, city: int = 0):
        """Поиск пользователей ВК со статусом в активном поиске по полу и городу России."""
        param = {'v': '5.131', 'access_token': self.token, 'count': 500, 'country_id': 1,
                 'city_id': city, 'sex': sex, 'status': 6, 'fields': 'relation, bdate, city'}
        return requests.get('https://api.vk.com/method/users.search', params=param).json()

    def get_sex(self, user_id: int) -> int:
        """Метод возвращает пол пользователя ВК.
        1-Женский, 2-Мужской, 0-Не указан"""
        sex = 0
        if user_id:
            param = {'user_ids': user_id, 'v': '5.131', 'access_token': self.token, 'fields': 'sex'}
            r = requests.get('https://api.vk.com/method/users.get', params=param).json()
            try:
                sex = r['response'][0]['sex']
            except KeyError:
                sex = 0
        return sex

    def get_city_id(self, user_id: int) -> int:
        """Метод возвращает id города, указанного на странице пользователя ВК.
        None - если город не указан"""
        city_id = None
        if user_id:
            param = {'user_ids': user_id, 'v': '5.131', 'access_token': self.token, 'fields': 'city'}
            r = requests.get('https://api.vk.com/method/users.get', params=param).json()
            try:
                city_id = r['response'][0]['city']['id']
            except KeyError:
                city_id = None
        return city_id

    def get_relation_id(self, user_id: int) -> int:
        """Метод возвращает id семейного положения пользователя ВК.
        1 — не женат/не замужем; 2 — есть друг/есть подруга; 3 — помолвлен/помолвлена; 4 — женат/замужем;
        5 — всё сложно; 6 — в активном поиске; 7 — влюблён/влюблена; 8 — в гражданском браке; 0 — не указано."""
        relation_id = 0
        if user_id:
            param = {'user_ids': user_id, 'v': '5.131', 'access_token': self.token, 'fields': 'relation'}
            r = requests.get('https://api.vk.com/method/users.get', params=param).json()
            try:
                relation_id = r['response'][0]['relation']
            except KeyError:
                relation_id = 0
        return relation_id

    def get_birthdate(self, user_id: int) -> datetime:
        """Метод возвращает дату рождения пользователя ВК, если она доступна в полном формате.
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
