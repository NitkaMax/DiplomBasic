from Yand import Yandex
from VK import Vk


if __name__ == '__main__':
    tokenvk = '188be8bee64dca2b2c654c821aab7c83af8771cb24c9dce53f73a019d88a589ebd1faed82c55ce69ca98a'
    tokenya = 'AQAAAABKsJ-SAADLW5usGNNGgkwRtZCCrjG-MKY'
    file_path = 'filename.json' 

    
    id = input('Введите id учетной записи Вконтакте: ')
    vk = Vk(tokenvk)
    print('Прогресс: Запрашиваю фото профиля с ID ' + (id))
    res = vk.get_photos_profile(id)
    if res == 'Error':
        print('Завершение работы')
    else:
        print('Прогресс: Данные от ID ' + (id) + ' получены')
        result = vk.sort_best_foto(res)
        print(f'Прогресс: Выбраны {len(result)} фото наилучшего разрешения')
        result = vk.rename_file_likes(result)
        print('Прогресс: Имена файлов подготвлены для записи на Яндекс.Диск')
        vk.create_json(result, file_path)
        print('Прогресс: Файл Json создан')


        dir_name = input('Назовите папку на Яндекс.Диске: ')
        ya = Yandex(tokenya)
        print('Прогресс: Создаем папку на Яндеск.Диске')
        ya.make_dir(dir_name)
        for i, foto in enumerate(result):
            print(f'Прогресс: загрузка {i + 1} фото из {len(result)}')
            ya.upload_file_url(dir_name, foto["file_name"], foto['url'])
        print('Прогресс: Запись JSON файла на Яндекс.Диск')
        ya.upload_file_path(dir_name, file_path)
        print('Прогресс: Программа выполнена')

