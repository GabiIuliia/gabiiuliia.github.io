# import configparser
# import datetime
# import json
# import os
# from data import db_session
# from data.users import User
# from data.news import News
# from forms.add_news import NewsForm
# from forms.user import RegisterForm
#
# import requests
#
# from data.users import User
#
# from flask import Flask, render_template, redirect, url_for, flash, request, abort
# from flask_login import LoginManager, login_user, logout_user, login_required
# from flask_login import current_user
#
# from data import db_session
# from loginform import LoginForm
# from ormbase import db
# from registrationform import RegistrationForm
import configparser
import datetime
import json
import os
from data import db_session
from data.users import User
from data.news import News
from forms.user import RegisterForm
from forms.add_news import NewsForm


import requests
from flask import Flask, url_for, request, render_template, abort, jsonify
from flask import flash, redirect, make_response, session
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_login import current_user
from werkzeug.utils import secure_filename

from forms.loginform import LoginForm
from mailform import MailForm
from ormbase import db
from registrationform import RegistrationForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)  # привязали менеджер авторизации к приложению


#
# app.config['SECRET_KEY'] = 'too_short_key'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

def configurate_app():
    app.config['SECRET_KEY'] = 'your_secret_key'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_database.db'  # Или другой URI для вашей базы данных
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()


# обработка ошибки сервера 401
# Пользователь не авторизован
# для просмотра данной страницы
@app.errorhandler(401)
def http_401_handler(error):
    return render_template('error401.html', title='Требуется аутентификация')


# обработка ошибки сервера 404
# Страница не найдена
@app.errorhandler(404)
def http_404_handler(error):
    return render_template('error404.html', title='Контент не найден')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter_by(email=form.email.data).first()
            print('user ' + user.__str__())
            if user and user.check_password(password=form.password.data):
                login_user(user, remember=form.remember_me.data, force=True)
                return redirect(url_for('success'))
            else:
                flash("Unknown user or wrong password")

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# создаем сессию по проверке в базе, есть ли он
@login_manager.user_loader
def user_loader(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# проверка сессии
# @app.route('/session_test')
# def session_test():
#     visit_count = session.get('visit_count', 0)
#     session['visit_count'] = visit_count + 1
#     # session.pop('visit_count', None) # если надо программно уничтожить сессию
#     return make_response(f'Вы посетили данную страницу {visit_count} раз.')
#
# проверка куки
# @app.route('/cookie_test')
# def cookie_test():
#     visit_count = int(request.cookies.get('visit_count', 0))
#     if visit_count:
#         res = make_response(f'Вы посетили данную страницу {visit_count + 1} раз')
#         res.set_cookie('visit_count', str(visit_count + 1), max_age=60 * 60 * 24 * 365 * 2)
#     else:
#         res = make_response('За последние два года вы посетили данную страницу впервые.')
#         res.set_cookie('visit_count', '1', max_age=60 * 60 * 24 * 365 * 2)
#         # res.set_cookie('visit_count', '1', max_age=0) # удаляем cookies
#     return res
#
#
@app.route('/news')
def news():
    with open("news.json", "rt", encoding="utf-8") as f:
        news_list = json.loads(f.read())
    print(news_list)
    return render_template('news.html', news=news_list, title='Новости')


# добавление новости
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/blog')
    return render_template('add_news.html', title='Добавление новости',
                           form=form)


# редактирование новости
@app.route('/blog/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()

        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
            form.submit.data = 'Отредактировать'
        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()

        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/blog')
        else:
            abort(404)
    return render_template('add_news.html', title='Редактирование новости',
                           form=form)

@app.route('/blog')
def blog():
    # if current_user.is_admin():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private == False)
    return render_template('blog.html', title='Новости', news=news)

# удаление новости
@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()

    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/blog')


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         if form.password.data != form.password_again.data:
#             return render_template('register.html', title='Регистрация',
#                                    form=form, message='Пароли не совпадают')
#         db_sess = db_session.create_session()
#         if db_sess.query(User).filter(User.email == form.email.data).first():
#             return render_template('register.html', title='Регистрация',
#                                    form=form, message=f'Пользователь с E-mail {form.email.data} уже есть')
#         user = User(
#             name=form.name.data,
#             email=form.email.data,
#             about=form.about.data
#         )
#         user.set_password(form.password.data)
#         db_sess.add(user)
#         db_sess.commit()
#         return redirect('/login')
#     return render_template('register.html', title='Регистрация', form=form)
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         user = db_sess.query(User).filter(User.email == form.email.data).first()
#         if user and user.check_password(form.password.data):
#             login_user(user, remember=form.remember_me.data)
#             return redirect('/')  # request.url- вернуться туда откуда пришел, либо на нужную страницу
#         return render_template('login.html', title='Ошибка авторизации',
#                                message='Неправильная пара: логин - пароль!',
#                                form=form)
#     return render_template('login.html', title='Авторизация', form=form)
#
#
# # 1. Добавить требуемый пункт в меню
# # 2. Создать .html-файл для расширения шаблона
# # 3. Отрендерить, создав соответствующий декоратор


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    password_hash=form.password.data)  # Не забудьте захешировать пароль!
        dbsession = db_session.create_session()
        user.set_password(form.password.data)
        dbsession.add(user)
        dbsession.commit()
        return redirect(url_for('index'))  # Перенаправляем на главную страницу
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/success')
def success():
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    db_session.global_init('db/property.db')
    configurate_app()
    app.run(debug=True)

# # http://localhost:5000/two-params/Victor/12
# @app.route('/two-params/<username>/<int:number>')
# def two_params_func(username, number):
#     param = 100 + number
#     return f"""
#     <h1>Пользователь: {username}</h1>
#     <h2>Номер в системе: {param}</h2>
#     """
#
# # Статический контент (в папке static/...)
# # Все изображения - static/images
# # Таблицы стилей - static/css
# # Шрифты - static/fonts
# # Любые файлы для скачивания
# # Файлы JS-сценариев - static/js
# # Музыка, видео
# # для удобства пользуемся url_for
# # Методы:
# # GET - запрашивает информацию с сервера, не меняя его состояния
# # POST - отправляет данные на сервер для обработки
# # PUT - заменяет текущие данные на сервере данными запроса
# # PATCH - частичная замена данных на сервере
# # DELETE - удаляет указанные данные

# # res = cur.execute("""select * from users
# #                   where id > 1 and email not like(%1%)""")
# # res.fetchall()
#
# if __name__ == '__main__':
#     db_session.global_init('db/blogs.db')
#     app.run(port=5000, host='127.0.0.1')
