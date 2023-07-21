import configparser

class Settings:
    def __init__(self, url='https://api.openweathermap.org', apikey='', lang='ru', units='metric'):
       self.url = url
       self.apikey = apikey
       self.lang = lang
       self.units = units

    def load_from_file(self, filename='settings.ini', section='OpenWeatherMap'):
        config = configparser.ConfigParser()
        config.read(filename)
        if config.has_section(section):
            self.url = config.get(section, 'url', fallback=self.url)
            self.apikey = config.get(section, 'apikey', fallback=self.apikey)
            self.lang = config.get(section, 'lang', fallback=self.lang)
            self.units = config.get(section, 'units', fallback=self.units)