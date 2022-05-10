from Yand import Yandex
from VK import Vk
from time import sleep
from tqdm import tqdm, tqdm_gui, trange



if __name__ == '__main__':
    for i in tqdm(__name__, desc="Запуск программы: ", leave=False):
        sleep(1)
    tokenvk = ''
    tokenya = ''
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
        result = vk.rename_by_num_of_likes(result)
        print('Прогресс: Имена файлов подготвлены для записи на Яндекс.Диск')
        vk.create_json(result, file_path)
        print('Прогресс: Файл Json создан')


        dir_name = input('Назовите папку на Яндекс.Диске: ')
        ya = Yandex(tokenya)
        print('Прогресс: Создаем папку на Яндеск.Диске')
        ya.create_dir(dir_name)
        for i, foto in enumerate(result):
            print(f'Прогресс: загрузка {i + 1} фото из {len(result)}')
            ya.upload_file_url(dir_name, foto["file_name"], foto['url'])
        # print('Прогресс: Запись JSON файла на Яндекс.Диск')
        ya.upload_file_path(dir_name, file_path)
        print('Прогресс: Программа выполнена')
#145053917
# 163404306



