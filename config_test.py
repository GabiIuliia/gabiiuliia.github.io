import configparser

config = configparser.ConfigParser()  # объект для обращения к ini

# читаем
config.read('settings.ini')

print(config['Telegram']['username'])
print(config['Telegram']['password'])

# создаём новую секцию
config.add_section('VK')
#         секция   ключ     значение
config.set('VK', 'vkuser', 'vk_pass')

with open('settings.ini', 'w', encoding='UTF-8') as f:
    config.write(f)
