from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import render_template, redirect
from forms.user import RegisterForm
from forms.user import LoginForm
from data.users import User
from data import db_session
from flask import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(User, user_id)


@app.route('/home')
def home():
    return 'список чатов'


@app.route('/<username>')
def profile(username):
    session = db_session.create_session()

    user = session.query(User).filter(User.username == username).first()

    if user:
        result = f'Профиль @{username}<br>Имя: {user.name}<br>'
        if user.about:
            result += f'О себе: {user.about}<br>'
        result += f'Дата регистрации: {user.created_date}'
    else:
        result = f'Пользователь {username} не найден'

    session.close()
    return result


@app.route('/chat/<username>')
def chat(username):
    return f'чат с {username}'


@app.route('/register', methods=['GET', 'POST'])
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

@app.route('/login', methods=['GET', 'POST'])
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

def main():
    db_session.global_init("db/profiles.db")
    app.run(port=8080, host='127.0.0.1')
    # app.run()


if __name__ == '__main__':
    main()
