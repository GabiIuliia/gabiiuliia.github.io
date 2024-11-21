from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from loginform import LoginForm
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
    form = LoginForm()
    if form.validate_on_submit():
        # Здесь должна быть логика для проверки пользователя
        return redirect(url_for('success'))
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)  # Не забудьте захешировать пароль!
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('base'))  # Перенаправляем на главную страницу
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/success')
def success():
    return redirect(url_for('base'))

if __name__ == '__main__':
    configurate_app()
    app.run(debug=True)