import requests
import datetime


class Vk:
    def __init__(self, token: str):
        self.token = token

    def search_potential_partners(self, sex: int = 0, city: int = 0):
        """Поиск пользователей ВК со статусом 'в активном поиске' по полу и городу России."""
        param = {'v': '5.131', 'access_token': self.token, 'count': 500, 'country_id': 1,
                 'city_id': city, 'sex': sex, 'status': 6, 'fields': 'relation, bdate, city'}
        return requests.get('https://api.vk.com/method/users.search', params=param).json()

    def get_user_info(self, user_id: int, name_case: str = 'nom') -> dict:
        """Метод возвращает словарь с информацией о пользователе ВК."""
        user_info = {}
        if user_id:
            param = {'user_ids': user_id, 'v': '5.131', 'access_token': self.token,
                     'fields': 'sex, city, relation, bdate', 'name_case': name_case}
            r = requests.get('https://api.vk.com/method/users.get', params=param).json()
            try:
                user_name = r['response'][0]['first_name'] + ' ' + r['response'][0]['last_name']
            except KeyError:
                user_name = None
            user_info['user_name'] = user_name
            try:
                sex = r['response'][0]['sex']
            except KeyError:
                sex = 0
            user_info['sex'] = sex
            try:
                city_id = r['response'][0]['city']['id']
            except KeyError:
                city_id = None
            user_info['city_id'] = city_id
            try:
                relation_id = r['response'][0]['relation']
            except KeyError:
                relation_id = 0
            user_info['relation_id'] = relation_id
            try:
                birthdate_str = r['response'][0]['bdate']
                if len(birthdate_str) > 5:
                    birthdate = datetime.datetime.strptime(birthdate_str, '%d.%m.%Y')
                else:
                    birthdate = None
            except KeyError:
                birthdate = None
            user_info['birthdate'] = birthdate
        return user_info

    def get_three_photos(self, user_id):
        """Метод подбирает 3 фотографии профиля с наибольшим количеством лайков и комментариев."""
        r = requests.get('https://api.vk.com/method/photos.get',
                         params={'owner_id': user_id, 'v': '5.131', 'access_token': self.token, 'extended': '1',
                                 'album_id': 'profile'})
        r = r.json()
        try:
            items = r['response']['items']
            photo_dict = {}
            for item in items:
                try:
                    likes = item['likes']['count']
                    comments = item['comments']['count']
                    media_id = item['id']
                    popularity = likes + comments
                    photo_dict[f'photo{user_id}_{media_id}'] = popularity
                except KeyError:
                    pass
            sort_by_popularity = sorted(photo_dict, key=photo_dict.get, reverse=True)
            three_photos = sort_by_popularity[0:3]
            return ','.join(three_photos)
        except KeyError:
            return None
