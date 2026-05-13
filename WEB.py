from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, emit, join_room
from data.communication_models import Chat, Message
# from flask import render_styled, redirect
from sqlalchemy.orm import joinedload
from jinja2 import TemplateNotFound

from flask import *
from flask import make_response
# from db import *
from data import db_session

from forms.user import RegisterForm
from forms.user import LoginForm
from data.users import User

website = Flask(__name__)
socketio = SocketIO(website, cors_allowed_origins="*")
website.config['SECRET_KEY'] = 'ваш-секретный-ключ-здесь'
login_manager = LoginManager()
login_manager.init_app(website)


# штука которая ищет старый шаблон, если нет то грузит новый
# теперь с куки
def render_styled(template_name, **kwargs):
    style = 'new'

    if current_user.is_authenticated:
        style = getattr(current_user, 'style', 'new')
    else:
        style = request.cookies.get('preferred_style', 'new')

    try:
        return render_template(f'{style}/{template_name}', **kwargs)
    except TemplateNotFound:
        return render_template(f'new/{template_name}', **kwargs)


@website.route('/')
def index():
    return redirect('/login')


@website.route('/home')
@login_required
def home():
    db_sess = db_session.create_session()

    chats = db_sess.query(Chat).filter((Chat.user1_id == current_user.id) | (Chat.user2_id == current_user.id)).all()

    chats_data = []
    for chat in chats:
        if chat.user1_id == current_user.id:
            companion = db_sess.query(User).get(chat.user2_id)
        else:
            companion = db_sess.query(User).get(chat.user1_id)

        last_message = db_sess.query(Message).filter(
            Message.chat_id == chat.id
        ).order_by(Message.created_date.desc()).first()

        chats_data.append({
            'username': companion.username,
            'name': companion.name,
            'last_message': last_message.text if last_message else "Нет сообщений",
            'chat_id': chat.id
        })
    db_sess.close()
    return render_styled('home.html', chats=chats_data)


@website.route('/<username>')
@login_required
def profile(username):
    db_sess = db_session.create_session()

    user = db_sess.query(User).filter(User.username == username).first()

    if not user:
        db_sess.close()
        return "Пользователь не найден", 404

    db_sess.close()
    return render_styled('profile.html', user=user)


@website.route('/chat/<username>')
@login_required
def chat(username):
    db_sess = db_session.create_session()
    try:
        user = db_sess.query(User).filter(User.username == username).first()

        if not user:
            return "Пользователь не найден", 404

        chat = db_sess.query(Chat).filter(
            ((Chat.user1_id == current_user.id) & (Chat.user2_id == user.id)) |
            ((Chat.user1_id == user.id) & (Chat.user2_id == current_user.id))).first()

        if not chat:
            return redirect(f'/create_chat/{username}')

        messages = db_sess.query(Message).options(
            joinedload(Message.user)).filter(Message.chat_id == chat.id).order_by(Message.created_date).all()

        messages_data = []
        for msg in messages:
            messages_data.append({
                'id': msg.id,
                'text': msg.text,
                'username': msg.user.username,
                'created_date': msg.created_date.strftime('%m-%d | %H:%M:%S'),
                'user_id': msg.user_id,
                'edited': msg.edited,
            })
        return render_styled('chat.html', user=user, messages=messages_data, chat_id=chat.id)


    finally:
        db_sess.close()


@website.route('/send_mess/<username>', methods=['POST'])
@login_required
def send_mess(username):
    try:
        db_sess = db_session.create_session()
        message_text = request.form.get('message')

        companion = db_sess.query(User).filter(User.username == username).first()

        chat = db_sess.query(Chat).filter(
            ((Chat.user1_id == current_user.id) & (Chat.user2_id == companion.id)) |
            ((Chat.user1_id == companion.id) & (Chat.user2_id == current_user.id))).first()

        if message_text and message_text.strip():
            msg = Message(text=message_text.strip(), user_id=current_user.id, chat_id=chat.id)
            db_sess.add(msg)
            db_sess.commit()
            print(f"✓ Сообщение сохранено: {message_text}")
    except Exception as e:
        if db_sess:
            db_sess.rollback()
        print(f"✗ Ошибка: {e}")
    finally:
        if db_sess:
            db_sess.close()
            print("Сессия закрыта")

    return redirect(f'/chat/{username}')


@website.route('/create_chat/<username>')
@login_required
def create_chat(username):
    db_sess = db_session.create_session()
    try:
        companion = db_sess.query(User).filter(User.username == username).first()
        if not companion:
            return "Пользователь не найден", 404

        existing_chat = db_sess.query(Chat).filter(
            ((Chat.user1_id == current_user.id) & (Chat.user2_id == companion.id)) |
            ((Chat.user1_id == companion.id) & (Chat.user2_id == current_user.id))
        ).first()

        print(f"Поиск чата: user1={current_user.id}, user2={companion.id}")
        print(f"Найден существующий чат: {existing_chat}")

        if existing_chat:
            print(f"Чат уже существует, перенаправляю на /chat/{username}")
            return redirect(f'/chat/{username}')

        chat = Chat(
            user1_id=current_user.id,
            user2_id=companion.id,
            name=f"Чат {current_user.name} и {companion.name}"
        )
        db_sess.add(chat)
        db_sess.commit()

        socketio.emit('new_chat', {
            'chat_id': chat.id,
            'username': companion.username,
            'name': companion.name,
            'last_message': 'Нет сообщений'
        }, room=f'user_{current_user.id}')

        socketio.emit('new_chat', {
            'chat_id': chat.id,
            'username': current_user.username,
            'name': current_user.name,
            'last_message': 'Нет сообщений'
        }, room=f'user_{companion.id}')

        return redirect(f'/chat/{username}')
    finally:
        db_sess.close()


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(User, user_id)


@website.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_confirm.data:
            return render_styled('register.html',
                                 title='Регистрация', form=form, message='пороли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.username == form.username.data).first():
            return render_styled('register.html',
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

    return render_styled('register.html', title='Регистрация', form=form)


@website.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/home")
        return render_styled('login.html',
                             message="Неправильный логин или пароль",
                             form=form)

    return render_styled('login.html', title='Авторизация', form=form)


# теперь с куки, сохраняет выбранный стиль
@website.route('/logout')
@login_required
def logout():
    style = current_user.style or 'new'
    logout_user()
    response = make_response(redirect('/login'))
    response.set_cookie('preferred_style', style, max_age=31536000)  # 1 год
    return response


@website.route('/search')
@login_required
def search_page():
    return render_styled('search.html')


# веб сокет
@socketio.on('connect')
def handle_connect():
    if not current_user.is_authenticated:
        return False
    join_room(f'user_{current_user.id}')


@socketio.on('join')
def on_join(data):
    chat_id = data['chat_id']
    db_sess = db_session.create_session()
    chat = db_sess.query(Chat).get(chat_id)
    if chat and (chat.user1_id == current_user.id or chat.user2_id == current_user.id):
        join_room(f'chat_{chat_id}')
    db_sess.close()


@socketio.on('send_message')
def handle_send_message(data):
    chat_id = data['chat_id']
    text = data['text'].strip()
    if not text:
        return
    db_sess = db_session.create_session()
    chat = db_sess.query(Chat).get(chat_id)
    if not chat or (chat.user1_id != current_user.id and chat.user2_id != current_user.id):
        db_sess.close()
        return
    msg = Message(text=text, user_id=current_user.id, chat_id=chat_id)
    db_sess.add(msg)
    db_sess.commit()

    emit('new_message', {
        'message_id': msg.id,
        'text': msg.text,
        'username': current_user.username,
        'created_date': msg.created_date.strftime('%m-%d | %H:%M:%S'),
        'user_id': current_user.id,
        'edited': False
    }, room=f'chat_{chat_id}')
    db_sess.close()

    socketio.emit('update_last_message', {
        'chat_id': chat_id,
        'text': msg.text,
        'username': current_user.username,
        'timestamp': msg.created_date.strftime('%m-%d | %H:%M:%S')
    }, room=f'user_{chat.user1_id}')

    socketio.emit('update_last_message', {
        'chat_id': chat_id,
        'text': msg.text,
        'username': current_user.username,
        'timestamp': msg.created_date.strftime('%m-%d | %H:%M:%S')
    }, room=f'user_{chat.user2_id}')


# хуйня чторбы редактировать профиль
@website.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    user.name = request.form.get('name', current_user.name)
    user.about = request.form.get('about', '')
    db_sess.commit()
    db_sess.close()
    return redirect('/' + current_user.username)


# поиск пользователей
@website.route('/api/search')
@login_required
def api_search():
    query = request.args.get('q', '').strip()
    if not query or len(query) < 1:
        return jsonify([])
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(
        (User.username == query) | (User.name.ilike(f'%{query}%'))
    ).filter(User.id != current_user.id).all()
    result = [{
        'username': u.username,
        'name': u.name,
        'about': u.about or ''
    } for u in users]
    db_sess.close()
    return jsonify(result)


# статус того что ты печатает
@socketio.on('typing_start')
def handle_typing_start(data):
    chat_id = data['chat_id']
    db_sess = db_session.create_session()
    chat = db_sess.query(Chat).get(chat_id)
    if chat and (chat.user1_id == current_user.id or chat.user2_id == current_user.id):
        emit('user_typing', {'username': current_user.username, 'chat_id': chat_id}, room=f'chat_{chat_id}',
             include_self=False)
    db_sess.close()


@socketio.on('typing_stop')
def handle_typing_stop(data):
    chat_id = data['chat_id']
    emit('user_stop_typing', {'username': current_user.username, 'chat_id': chat_id}, room=f'chat_{chat_id}',
         include_self=False)


# редактирование сообщений
@socketio.on('edit_message')
def handle_edit_message(data):
    msg_id = int(data['message_id'])
    chat_id = int(data['chat_id'])
    new_text = data['text'].strip()
    if not new_text:
        return
    db_sess = db_session.create_session()
    msg = db_sess.query(Message).get(msg_id)
    if msg and msg.user_id == current_user.id and msg.chat_id == chat_id:
        msg.text = new_text
        msg.edited = True
        db_sess.commit()
        emit('message_edited', {
            'message_id': msg_id,
            'text': new_text,
            'edited': True,
            'chat_id': chat_id
        }, room=f'chat_{chat_id}')
    db_sess.close()


# удаляние сообщений
@socketio.on('delete_message')
def handle_delete_message(data):
    msg_id = int(data['message_id'])
    chat_id = int(data['chat_id'])
    db_sess = db_session.create_session()
    msg = db_sess.query(Message).get(msg_id)
    if msg and msg.user_id == current_user.id and msg.chat_id == chat_id:
        db_sess.delete(msg)
        db_sess.commit()
        emit('message_deleted', {
            'message_id': str(msg_id),
            'chat_id': chat_id
        }, room=f'chat_{chat_id}')
    db_sess.close()


# шаблны
@website.context_processor
def inject_style():
    style = 'new'
    if current_user.is_authenticated:
        style = current_user.style or 'new'
    return {'current_style': style}


@website.route('/set_style', methods=['POST'])
@login_required
def set_style():
    new_style = request.form.get('style', 'new')
    if new_style in ('new', 'old'):
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        user.style = new_style
        db_sess.commit()
        db_sess.close()

        # сохранение запроса в куки
        response = make_response(redirect(request.referrer or '/home'))
        response.set_cookie('preferred_style', new_style, max_age=31536000)
        return response
    return redirect(request.referrer or '/home')


# аватарка
@website.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    file = request.files.get('avatar')
    if not file or not file.filename:
        return redirect('/' + current_user.username)

    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    if size > 10 * 1024 * 1024:
        return "ДА Че ты грузишь мне тут. принимаю не больше — 10 МБ.", 413

    import os, uuid
    avatars_dir = 'static/avatars'
    os.makedirs(avatars_dir, exist_ok=True)

    ext = file.filename.rsplit('.', 1)[-1].lower()
    filename = f"user_{current_user.id}_{uuid.uuid4().hex[:8]}.{ext}"
    filepath = os.path.join(avatars_dir, filename)
    file.save(filepath)

    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    user.avatar = f"avatars/{filename}"
    db_sess.commit()
    db_sess.close()

    return redirect('/' + current_user.username)
