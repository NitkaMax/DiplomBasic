import requests
from error_code import error_request

class Yandex():
    def __init__(self, token):
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'OAuth {token}'
        }

    def create_dir(self, dir_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': dir_name}
        response = requests.put(url, headers=self.headers, params=params, timeout=5)
        if response.status_code == 201:
            print('Прогресс: Код ответа - 201 - папка на Яндекс.Диске создана корректно')
        else:
            error_request(response.status_code)
            print('Ошибка ответа сервера')

    def upload_file_url(self, dir_name, file_name, url_file):
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {
            'path': f'/{dir_name}/{file_name}',
            'url': url_file
        }
        response = requests.post(url, params=params, headers=self.headers, timeout=5)
        if response.status_code == 202:
            print('Прогресс: Код ответа - 202 - фото загружено')
        else:
            error_request(response.status_code)
            print('Ошибка ответа сервера')

    def upload_file_path(self, dir_name, file_path):
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {
            'path': f'/{dir_name}/{file_path}',
            'overwrite': 'true'
        }
        response = requests.get(url, headers=self.headers, params=params, timeout=5)
        if response.status_code == 200:
            print('Прогресс: Код ответа - 200 - Запрос отработан корректно')
            dic = response.json()
            response = requests.put(dic['href'], data=open(file_path, 'rb'), headers=self.headers, timeout=5)
            if response.status_code == 201:
                print('Прогресс: Код ответа - 201 - Файл JSON успешно записан на Я-Диск')
            else:
                error_request(response.status_code)
                print('Ошибка ответа сервера')
        else:
            error_request(response.status_code)
            print('Ошибка ответа сервера')