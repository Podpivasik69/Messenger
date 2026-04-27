from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField('Уникальное имя пользователя', validators=[DataRequired()])
    name = StringField("Отображаемое имя", validators=[DataRequired()])
    about = TextAreaField('О себе')
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_confirm = PasswordField('Введите пароль еще раз', validators=[DataRequired()])
    submit = SubmitField('ЗАрегистрироваться')


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField("Войти")
