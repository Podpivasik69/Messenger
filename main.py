from flask import Flask
from data import db_session
from data.users import User
import WEB


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/profiles.db")
    db_sess = db_session.create_session()


    # user = db_sess.query(User).filter(User.username == 'danil').first()
    # db_sess.delete(user)

    user = User()
    user.name = "данил колбасенко"
    user.about = "стендофф2"
    user.username = "danil"
    user.hashed_password = '123'

    db_sess.add(user)

    db_sess.commit()

    WEB.website.run(port=8080, host='127.0.0.1')
    # app.run()


if __name__ == '__main__':
    main()
