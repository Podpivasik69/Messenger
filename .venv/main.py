from flask import Flask
from data import db_session
from data.users import User
import WEB


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/profiles.db")
    WEB.website.run(port=8080, host='127.0.0.1')
    # app.run()


if __name__ == '__main__':
    main()
