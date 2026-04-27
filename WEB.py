from flask import *
from db import *
from data import db_session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import render_template, redirect
from forms.user import RegisterForm
from forms.user import LoginForm
from data.users import User
from data.communication_models import Chat, Message
from sqlalchemy.orm import joinedload



website = Flask(__name__)
website.config['SECRET_KEY'] = 'ваш-секретный-ключ-здесь'
login_manager = LoginManager()
login_manager.init_app(website)

@website.route('/')
def index():
    return redirect('/home')

@website.route('/home')
def home():
    db_sess = db_session.create_session()
    # chats = [
    #     {'username': 'test_1', 'name': 'Пользователь 1', 'last_message': 'Привет!'},
    #     {'username': 'test_2', 'name': 'Пользователь 2', 'last_message': 'Как дела?'},
    # ]
    chats = [
        db_sess.query(User).filter(User.username == 'mixas').first(),
        db_sess.query(User).filter(User.username == 'mixa2').first()
    ]

    db_sess.close()
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

    db_sess.close()
    return result

@website.route('/chat/<username>')
def chat(username):
    db_sess = db_session.create_session()
    comm_sess = db_session.create_comm_session()
    try:
        user = db_sess.query(User).filter(User.username == username).first()
        messages = comm_sess.query(Message).options(
            joinedload(Message.user)).filter(Message.user_id == 1).all()
        messages_data = []
        for msg in messages:
            messages_data.append({
                'text': msg.text,
                'username': user.username,
                'created_date': msg.created_date.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': msg.user_id
            })

        return render_template('chat.html', username=username, messages=messages_data)

    finally:
        db_sess.close()
        comm_sess.close()


@website.route('/send_mess/<username>', methods=['POST'])
def send_mess(username):
    comm_sess = None
    try:
        comm_sess = db_session.create_comm_session()
        message_text = request.form.get('message')
        if message_text and message_text.strip():
            msg = Message(text=message_text.strip(), user_id=1, chat_id=1)
            comm_sess.add(msg)
            comm_sess.commit()
            print(f"✓ Сообщение сохранено: {message_text}")
    except Exception as e:
        if comm_sess:
            comm_sess.rollback()
        print(f"✗ Ошибка: {e}")
    finally:
        if comm_sess:
            comm_sess.close()
            print("Сессия закрыта")

    return redirect(f'/chat/{username}')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(User, user_id)

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
            return redirect("/home")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@website.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


