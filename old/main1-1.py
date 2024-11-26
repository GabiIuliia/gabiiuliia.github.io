from flask import Flask, url_for, request, render_template
import json

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    param = {}
    param['text'] = 'Этот текст отобразится на главной странице'
    param['title'] = 'Главная'
    return render_template('index.html', **param)
    # return """
    # <a href="/index">Главная</a> | <a href="/contacts">Контакты</a> | <a href="/img/1">Картинка 1</a>
    # | <a href="/img/2">Картинка 2</a>
    # """


@app.route('/news')
def news():
    with open("news.json", "rt", encoding="utf-8") as f:
        news_list = json.loads(f.read())
    print(news_list)
    return render_template('news.html', news=news_list, title='Новости')


@app.route('/pets')
def pets():
    with open('pets.json', 'rt', encoding='utf-8') as f:
        pets_info = json.load(f)
    print(pets_info)
    return render_template('pets.html', pets=pets_info, title='Питомцы')


@app.route('/queue')
def queue():
    return render_template('queue.html', title='Очередь на медосмотр')


@app.route('/odd_even/', defaults={'num': 0})
@app.route('/odd_even/<int:num>')
def odd_even(num):
    return render_template('index.html', num=num, title='Чётное или нечётное')


@app.route('/countdown')
def countdown():
    cl = ['Старт']
    cl += [str(x) for x in reversed(range(11))]
    cl.append('Финиш')
    return '<br>'.join(cl)

# 1. Добавить требуемый пункт в меню
# 2. Создать .html-файл для расширения шаблона
# 3. Отрендерить, создав соответствующий декоратор
@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Наши контакты')


@app.route('/about')
def about():
    params = {}
    params['title'] = 'О нас'
    params['text'] = 'Мы перспективная и динамично развивающаяся компания...'
    return render_template('about.html', **params)


# Статический контент (в папке static/...)
# Все изображения - static/images
# Таблицы стилей - static/css
# Шрифты - static/fonts
# Любые файлы для скачивания
# Файлы JS-сценариев - static/js
# Музыка, видео
# для удобства пользуемся url_for
@app.route('/img/', defaults={'num': None})
@app.route('/img/<num>')
def show_img(num):
    """
    :param num: по умолчанию - строка
    <int:num> - целое число
    <float:num> - действительное число
    <path:num> - строка со слешами для URL
    <uuid:num> - идентификатор в 16-м представлении (550e8400-e29b-41d4-a716-446655440000)
    :return: Путь к картинке
    """
    # num += 1
    if num:
        return f"""
        <h1>Python</h1>
        <img src="{url_for('static', filename=f'images/python-{num}.jpg')}"><br>
        <a href='/'>На главную</a>
        """
    else:
        return f"""
                <h1>Здесь ничего нет.</h1>
                <img src="{url_for('static', filename='images/python.png')}"><br>
                <a href='/'>На главную</a>
                """


# http://localhost:5000/two-params/Victor/12
@app.route('/two-params/<username>/<int:number>')
def two_params_func(username, number):
    param = 100 + number
    return f"""
    <h1>Пользователь: {username}</h1>
    <h2>Номер в системе: {param}</h2>
    """


# Методы:
# GET - запрашивает информацию с сервера, не меняя его состояния
# POST - отправляет данные на сервер для обработки
# PUT - заменяет текущие данные на сервере данными запроса
# PATCH - частичная замена данных на сервере
# DELETE - удаляет указанные данные
@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return """
        <!DOCTYPE html>
<html lang="ru">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Заполните форму</title>
    <link type="image/png" sizes="32x32" rel="icon" href="images/favicon.png">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <link type="text/css" rel="stylesheet" href="css/style.css">
</head>

<body>
<!--главный контейнер-->
<div class="container">
    <h1>Форма для регистрации</h1>
    <form class="login_form" method="post">
        <input class="form-control" type="email" name="email" id="email" placeholder="Введите E-mail">
        <input class="form-control" type="password" name="password" id="password">
        <label for="profSelect">Ваша профессия</label>
        <select class="form-control" name="profession" id="profSelect">
            <option>Инженер</option>
            <option>Конструктор</option>
        </select>
        <button type="submit" class="btn btn-primary">Отправить</button>
    </form>
</div>
<!--главный контейнер (end)-->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
        crossorigin="anonymous"></script>
</body>

</html>
        """
    elif request.method == 'POST':
        return f"""
        <!DOCTYPE html>
<html lang="ru">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Заполните форму</title>
    <link type="image/png" sizes="32x32" rel="icon" href="images/favicon.png">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <link type="text/css" rel="stylesheet" href="css/style.css">
</head>

<body>
<!--главный контейнер-->
<div class="container">
    <h1>Вот, что Вы отправили:</h1>
    <p><b>Ваш Email</b>: {request.form['email']}</p>
    <p><b>Пароль</b>: {request.form['password']}</p>
    <p><b>Ваша профессия:</b> {request.form['profession']}</p>
</div>
<!--главный контейнер (end)-->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
        crossorigin="anonymous"></script>
</body>

</html>
    """


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
