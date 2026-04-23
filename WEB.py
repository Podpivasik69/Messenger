from flask import *
from db import *
from data.users import User
from data import db_session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import render_template, redirect
from forms.user import RegisterForm
from forms.user import LoginForm
from data.users import User


website = Flask(__name__)
website.config['SECRET_KEY'] = 'ваш-секретный-ключ-здесь'

@website.route('/home')
def home():
    db_sess = db_session.create_session()
    # chats = [
    #     {'username': 'test_1', 'name': 'Пользователь 1', 'last_message': 'Привет!'},
    #     {'username': 'test_2', 'name': 'Пользователь 2', 'last_message': 'Как дела?'},
    # ]
    chats = [
        db_sess.query(User).filter(User.username == 'test_1').first()
    ]

    db_sess.close
    return render_template('home.html', chats=chats)

@website.route('/<username>')
def profile(username):
    db_sess = db_session.create_session()

    user = db_sess.query(User).filter(User.username==username).first()

    if user:
        result = f'Профиль @{username}<br>Имя: {user.name}<br>'
        if user.about:
            result += f'О себе: {user.about}<br>'
        result += f'Дата регистрации: {user.created_date}'
    else:
        result = f'Пользователь {username} не найден'

    db_sess.close
    return result

@website.route('/chat/<username>')
def chat(username):
    db_sess = db_session.create_session()

    messages = [db_sess.query(User).filter(User.username == username).first()]

    db_sess.close
    return render_template('chat.html', username=username, messages=messages)

@website.route('/send_mess/<username>', methods=['GET', 'POST'])
def send_mess(username):
    db_sess = db_session.create_session()

    message = request.form.get('message')

@website.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_confirm.data:
            return render_template('register.html',
                                   title='Регистрация', form=form, message='пороли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.username == form.username.data).first():
            return render_template('register.html',
                                   title='Регистрация', form=form,
                                   message='ПОльзователь с таким именнем уже существуеи')
        user = User()
        user.username = form.username.data
        user.name = form.name.data
        user.about = form.about.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)

@website.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)
