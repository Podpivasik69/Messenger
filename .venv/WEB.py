from flask import *
from db import *
from data.users import User
from data import db_session


website = Flask(__name__)

@website.route('/home')
def home():
    return 'список чатов'

@website.route('/<username>')
def profile(username):
    session = db_session.create_session()

    user = session.query(User).filter(User.username==username).first()

    if user:
        result = f'Профиль @{username}<br>Имя: {user.name}<br>'
        if user.about:
            result += f'О себе: {user.about}<br>'
        result += f'Дата регистрации: {user.created_date}'
    else:
        result = f'Пользователь {username} не найден'

    session.close
    return result

@website.route('/chat/<username>')
def chat(username):
    return f'чат с {username}'

