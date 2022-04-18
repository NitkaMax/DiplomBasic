import requests
import time
import json
from error_code import error_request
from pprint import pprint

class Vk():
    def __init__(self, token):
        self.token = token

    def get_photos_profile(self, id):
        URL = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': id.strip(),
            'album_id': 'profile',
            'extended': True,
            'photo_sizes': True,
            'access_token': self.token,
            'v': '5.131'
        }
        res = requests.get(URL, params=params, timeout=5)
        if res.status_code == 200:
            print('Прогресс: 200 - Получен корректный ответ от сервера')
            error_test = res.json().get('error')  # проверка приватности
            if error_test != None:
                error_code_vk(error_test.get('error_code'))
                res = 'Error'
        else:
            error_request(res.status_code)
            print('Ошибка ответа сервера')
            res = 'Error'
        return res

    def sort_best_foto(self, res):

        TypeSize = ('w', 'z', 'y', 'x', 'r', 'q', 'p', 'o', 'm', 's')  
        result = []
        for j in range(len(res.json()['response']['items'])):
            size_max = 10
            for i in range(len(res.json()['response']['items'][j]['sizes'])):
                size = res.json()['response']['items'][j]['sizes'][i]['type']
                if size_max > TypeSize.index(size):
                    size_max = TypeSize.index(size)
                    url_foto = res.json()['response']['items'][j]['sizes'][i]['url']
            dic_res = {
                "file_name": f"{res.json()['response']['items'][j]['likes']['count']}.jpg",
                "size": TypeSize[size_max],
                "url": url_foto,
                "date": res.json()['response']['items'][j]['date'],
                "likes": res.json()['response']['items'][j]['likes']['count']
            }
            result.append(dic_res)
        return result

    def rename_by_num_of_likes(self, result):
        likes = []
        for like in result:
            likes.append(like['likes'])
        likes_unique = list(set(likes))
        for like in likes_unique:
            likes.remove(like)
        likes = list(set(likes))
        print('Прогресс: Количество лайков по каждой фото получено')
        for file_name in result:
            for like in likes:
                if like == file_name['likes']:
                    time_name = time.localtime(file_name["date"])
                    file_name['file_name'] = f'{like} {time_name.tm_mday}.{time_name.tm_mon}.{time_name.tm_year}.jpg'
        return result

    def create_json(self, result, file_path):
        json_tmp = []
        for i in result:
            dic_tmp = {}
            dic_tmp['file_name'] = i['file_name']
            dic_tmp['size'] = i['size']
            json_tmp.append(dic_tmp)
        with open(file_path, 'w') as f:
            json.dump(json_tmp, f)

def error_code_vk(error):
    error_dic = {
        1 : 'Произошла неизвестная ошибка.',
        2 : 'Приложение выключено.',
        3 : 'Передан неизвестный метод.',
        4 : 'Неверная подпись.',
        5 : 'Авторизация пользователя не удалась.',
        6 : 'Слишком много запросов в секунду.',
        7 : 'Нет прав для выполнения этого действия.',
        8 : 'Неверный запрос.',
        9 : 'Слишком много однотипных действий.',
        10 : 'Произошла внутренняя ошибка сервера.',
        11 : 'В тестовом режиме приложение должно быть выключено или пользователь должен быть залогинен.',
        14 : 'Требуется ввод кода с картинки (Captcha).',
        15 : 'Доступ запрещён.',
        16 : 'Требуется выполнение запросов по протоколу HTTPS, т.к. пользователь включил настройку, требующую работу через безопасное соединение',
        17 : 'Требуется валидация пользователя',
        18 : 'Страница удалена или заблокирована.',
        20 : 'Данное действие запрещено для не Standalone приложений',
        21 : 'Данное действие разрешено только для Standalone и Open API приложений.',
        23 : 'Метод был выключен.',
        24 : 'Требуется подтверждение со стороны пользователя',
        27 : 'Ключ доступа сообщества недействителен',
        28 : 'Ключ доступа приложения недействителен.',
        29 : 'Достигнут количественный лимит на вызов метода',
        30 : 'Профиль является приватным',
        100 : 'Один из необходимых параметров был не передан или неверен',
        101 : 'Неверный API ID приложения.',
        113 : 'Неверный идентификатор пользователя',
        150 : 'Неверный timestamp',
        200 : 'Доступ к альбому запрещён',
        201 : 'Доступ к аудио запрещён',
        203 : 'Доступ к группе запрещён.',
        300 : 'Альбом переполнен',
        500 : 'Действие запрещено. Вы должны включить переводы голосов в настройках приложения.',
        600 : 'Нет прав на выполнение данных операций с рекламным кабинетом.',
        603 : 'Произошла ошибка при работе с рекламным кабинетом'
    }
    pprint(f'Прогресс: {error_dic[error]} - код ошибки VK - {error}')