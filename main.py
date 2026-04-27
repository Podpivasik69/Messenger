from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import render_template, redirect
from forms.user import RegisterForm
from forms.user import LoginForm
from data.users import User
from data import db_session
from flask import *
import WEB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

def main():
    db_session.global_init("db/profiles.db")
    db_session.comm_global_init("db/communications.db")
    WEB.website.run(port=8080, host='127.0.0.1')
    # app.run()


if __name__ == '__main__':
    main()
