from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError

from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
        Length(1, 64, message="Nazwa użytkownika musi mieć minimum 1 znak i maksimum 64 znaki."),
        Email(message="Nieprawidłowy adres email.")])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Pozostaw zalogowanym')
    submit = SubmitField('Zaloguj')
    submit.label = None

class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(),
        Length(1, 64, message="Nazwa użytkownika musi mieć minimum 1 znak i maksimum 64 znaki.")])
    email = StringField('Email', validators=[DataRequired(),
        Length(1, 64, message="Adres email nie może być dłuższy, niż 64 znaki."),
        Email(message="Nieprawidłowy adres email.")])
    password = PasswordField('Hasło', validators=[DataRequired(),
        Length(8, message="Hasło musi mieć minimum 8 znaków."),
        EqualTo('password_check', message='Hasła muszą się zgadzać.')])
    password_check = PasswordField('Powtórz hasło', validators=[DataRequired()])
    submit = SubmitField('Zarejestruj')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Istnieje już konto z takim adresem email.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data.lower()).first():
            raise ValidationError('Ta nazwa użytkownika jest już zajęta.')
