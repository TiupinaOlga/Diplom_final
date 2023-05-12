import datetime

import vk_api
from vk_api.exceptions import ApiError
from datetime import date

from operator import itemgetter  # для сортировки словаря

class VkTools():
    def __init__(self, token):
        self.ext_api = vk_api.VkApi(token=token)

    """Функция для получения информации о пользователе"""

    def get_profile_info(self, user_id):
        try:
            info = self.ext_api.method('users.get',
                                       {'user_id': user_id,
                                        'fields': 'bdate, city,sex,relation'
                                        }
                                       )
        except ApiError:
            return
        return info

    """Функция для поиска пары для поьзователя"""

    def user_search(self, city_id, age_from, age_to, sex, status=None, offset=None):
        try:
            profiles = self.ext_api.method('users.search',
                                           {'city_id': city_id,
                                            'age_from': age_from,
                                            'age_to': age_to,
                                            'sex': sex,
                                            'count': 50,
                                            'offset': offset,
                                            'status': status
                                            }
                                           )
        except ApiError:
            return

        profiles = profiles['items']

        result = []
        for profile in profiles:
            if profile['is_closed'] == False:
                result.append({'name': profile['first_name'] + ' ' + profile['last_name'],
                               'id': profile['id']
                               })
        return result

    """Функция для получения массива данных о фото пользователя"""

    def photos_get(self, user_id):
        photos = self.ext_api.method('photos.get',
                                     {'album_id': 'profile',
                                      'owner_id': user_id,
                                      'extended': 1
                                      })

        try:
            photos = photos['items']
        except KeyError:
            return

        photos_sort = []
        for num, photo in enumerate(photos):
            photos_sort.append({'owner_id': photo['owner_id'],
                                'id': photo['id'],
                                'media': (f'photo{photo["owner_id"]}_{photo["id"]}'),
                                'likes': photo['likes']['count'] + photo['comments']['count']})

        photos_sort.sort(
            key=itemgetter('likes'))  # отсортированный список словарей с данными по фото - надо взять последние 3
        photos_sort = photos_sort[::-1]  # переворачиваем список вобратном порядке

        result = []  # возвращаем топ-3
        for num, photos_sort in enumerate(photos_sort):
            result.append({'owner_id': photos_sort['owner_id'],
                           'id': photos_sort['id'],
                           'media': photos_sort['media']})
            if num == 2:
                break
        return result

    """Функция для вычисления возраста пользователя"""

    def get_age(self, user_id):  # вычисление возраста пользователя, который ведет поиск
        info = self.get_profile_info(user_id)
        bdate = info[0]['bdate']
        if len(bdate) == 10:  # если указан год рождения
            bdate = datetime.datetime.strptime(bdate, '%d.%m.%Y')
            today = date.today()
            return today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))
        else:
            return 0

    """Функция для определения пола пользователей"""

    def get_sex_for_search(self, user_id):  # пол человека для поиска
        info = self.get_profile_info(user_id)
        sex = info[0]['sex']  # пол пользователя, который ищет
        if sex == 1:
            return 2
        elif sex == 2:
            return 1
        else:
            return 0

    """Функция для определения id города из профиля"""

    def get_city_id(self, user_id):  # получение id города пользователя из профиля
        info = self.get_profile_info(user_id)
        if 'city' in info[0]:
            return info[0]['city']['id']
        else:
            return 0

    """Функция для определения id города из сообщения"""

    def search_city_id(self, q):  # поиск id города, который ввел пользователь для поиска
        try:
            city = self.ext_api.method('database.getCities',
                                       {'q': q,
                                        }
                                       )
        except ApiError:
            return
        if city['count'] != 0:
            return city['items'][0]['id']
        else:
            return 0
