import configparser

config = configparser.ConfigParser()  # объект для обращения к ini

# читаем
config.read('settings.ini')
