from flask import Flask, url_for, request, render_template
from mail_sender import send_mail
from mailform import MailForm
from loginform import LoginForm
from werkzeug.utils import secure_filename
import json, os

current_directory = os.path.dirname(__file__)  # путь к корню сервера
UPLOAD_FOLDER = f'{current_directory}/static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'too_short_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# если справа от точки стоит нужное расширение из прописанного в ALLOWED_EXTENSIONS , то вернуть правду

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login-1.html', title='Авторизация', form=form)


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = MailForm()
    if form.validate_on_submit():
        name = form.username.data
        phone = form.username.data
        email = form.email.data
        message = form.message.data

        text = f"""
        Пользователь {name} оставил вам сообщение
        {message}
        Телефон {phone}
        Почта {email}
            """
        send_mail('iuliiazluka@yandex.ru', 'Заявка с сайта', text)
        return redirect('/success')
    return render_template('mailform.html', title='Заявка', form=form)


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'GET':
        return render_template('weather.html', title='Погода', form=None)
    elif request.method == 'POST':
        config.read('settings.ini')
        city = request.form['city']
        if len(city) < 2:
            flash('Город не введен или введен не полностью')
            return redirect(request.url)
        key = config['Weather']['key']
        # return render_template('weather.html', title=f'Погода в городе {city}', form=request.form)

    res = requests.get('http://api.openweathermap.org/',
                       params={'q': 'Санкт Петербург',
                               'type': 'like',
                               'units': 'metric',
                               'APPID': key})
    data = res.json()
    print(data)
    if len(data['list']) == 0:
        flash('Город введен не верно')
        return redirect(request.url)

    temp = data['list'][0]['main']  # читаем из data=res.json
    params = {}  # пустой словарь для передачи параметров в render weather.html
    params['temper'] = temp['temp']
    params['feel'] = temp['feels_like']
    params['press'] = temp['pressure']
    params['humid'] = temp['humidity']

    return render_template('weather.html', title=f'Погода в городе {city}', form=request.form, params=params)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html', title='Выбор файла', form=None)
    elif request.method == 'POST':
        if 'file' not in request.files:
            flash('Файл не был прочитан')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Файл не был отправлен')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('Загрузка файлов данного типа запрещена!')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('upload.html', title='Файл загружен',
                                   form=True)


@app.route('/success')
def success():
    return 'Успех'


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
        return render_template('form_sample.html', title='Заполните форму', form='None')

    elif request.method == 'POST':
        return render_template('form_sample.html', title='Ваши данные', form=request.form)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
