from openweathermap import OpenWeatherMap
from settings import Settings
from threading import Thread

# Написать программу запроса погоды
# 1. Создать класс для хранения параметров погоды.
# 2. Открыть файл cities.txt с названием городов, считать города и загрузить в программу список городов.
# 3. По считанным городам параллельно (асинхронно) запросить на openweatherAPI информацию о погоде

if __name__ == '__main__':
    # Перед тестированием нужно заполнить apikey в настройках файла settings.ini
    # или передать при создании объекта класса Settings
    Settings = Settings()
    Settings.load_from_file()

    OpenWeatherMap = OpenWeatherMap(Settings)
    list_cities = OpenWeatherMap.get_list_cities()

    # For test
    t1 = Thread(target=OpenWeatherMap.add_to_list, args=[list_cities[0]['id']])
    t1.run()
    t2 = Thread(target=OpenWeatherMap.add_to_list, args=[list_cities[1]['id']])
    t2.run()
    t3 = Thread(target=OpenWeatherMap.add_to_list, args=[list_cities[2]['id']])
    t3.run()

    # Load full list of city
    # for city_item in list_cities:
    #     t = Thread(target=OpenWeatherMap.get_info_for_city, args=city_item['id'])
    #     t.run()

    OpenWeatherMap.save_to_file()
