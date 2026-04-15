from flask import *
from db import *
from data.users import User


website = Flask(__name__)

@website.route('/home')
def home():
    return 'список чатов'

@website.route('/<username>')
def profile(username):
    return f'профиль {username}'

@website.route('/chat/<username>')
def chat(username):
    return f'чат с {username}'

