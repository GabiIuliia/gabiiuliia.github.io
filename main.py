from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from baza import User
from loginform import LoginForm
from ormbase import db
from registrationform import RegistrationForm

app = Flask(__name__)


def configurate_app():
    app.config['SECRET_KEY'] = 'your_secret_key'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_database.db'  # Или другой URI для вашей базы данных
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', title='Авторизация', form=form)
    elif request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            # Здесь должна быть логика для проверки пользователя
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.password_hash == form.password.data:
                return redirect(url_for('success'))
        else:
            return redirect('/login')
    else:
        return redirect('/login')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     #user = db.session.get(User)
#     #if user is not None:
#     #    print("user " +user.username)
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Здесь должна быть логика для проверки пользователя
#         return redirect(url_for('success'))
#     return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data, password_hash=form.password.data)  # Не забудьте захешировать пароль!
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))  # Перенаправляем на главную страницу
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/success')
def success():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    configurate_app()
    app.run(debug=True)