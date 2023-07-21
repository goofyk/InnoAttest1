import json
from settings import Settings
import urllib.request
import gzip, shutil, os, string
import requests

class OpenWeatherMap:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.cities = []

    def get_list_cities(self, country = 'RU') -> list:
        filename_json = self.__save_list_cities()
        with open(filename_json, 'r', encoding='utf-8') as file_json:
            list_cities = []
            data_json = json.load(file_json)
            for str_json in data_json:
                if str_json['country'] == country:
                    list_cities.append(str_json)
        file_json.close()
        os.remove(filename_json)
        return list_cities

    def __save_list_cities(self) -> string:
        filename_gz = 'city.list.min.json.gz'
        filename_json = filename_gz.split('.')
        filename_json.remove('gz')
        filename_json = '.'.join(filename_json)
        urllib.request.urlretrieve("http://bulk.openweathermap.org/sample/" + filename_gz, filename_gz)
        with gzip.open(filename_gz, 'rb') as f_in:
            with open(filename_json, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            f_out.close()
        f_in.close()
        os.remove(filename_gz)
        return filename_json

    def get_info(self, city_id=None, city_name=None) -> dict:
        if not city_id == None:
            req_address = f'/data/2.5/weather?id={city_id}'\
                      f'&appid={self.settings.apikey}'\
                      f'&units={self.settings.units}'\
                      f'&lang={self.settings.lang}'
        elif not city_name == None:
            req_address = f'/data/2.5/weather?q={city_name}' \
                          f'&appid={self.settings.apikey}' \
                          f'&units={self.settings.units}' \
                          f'&lang={self.settings.lang}'
        response = requests.get(self.settings.url + req_address)
        data_json = response.json()
        return data_json

    def add_to_list(self, city_id):
        city_info = self.get_info(city_id=city_id)
        city_element = {
            "Город": city_info.get("name"),
            "Погода": {
                "Температура": city_info.get("main").get("temp"),
                "Скорость ветра": city_info.get("wind").get("speed"),
                "Описание": city_info.get("weather")[0].get("description")
            }
        }
        self.cities.append({city_id: city_element})

    def save_to_file(self, filename='city.list.weather.json'):
        with open(filename, 'w', encoding='utf-8', newline='\r\n') as fp:
            json.dump(self.cities, fp, ensure_ascii=False)
        fp.close()