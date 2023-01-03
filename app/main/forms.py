from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms import ValidationError
from wtforms.widgets import TextArea


class CarForm(FlaskForm):
    make = StringField('Marka', validators=[DataRequired(),
        Length(1, 20, message="Marka samochodu musi być uzupełniona."),])
    model = StringField('Model', validators=[DataRequired(),
        Length(1, 20, message="Model samochodu musi być uzupełniony."),])
    combustion = DecimalField('Spalanie', places=1, validators=[DataRequired(),],
        render_kw={"step": "0.1"})
    fuel = SelectField(u'Rodzaj paliwa', validators=[DataRequired(),])
    submit = SubmitField('Dodaj')
    submit.label = None


class CommentForm(FlaskForm):
    rate = DecimalField('Ocena', places=1, validators=[Optional(),\
        NumberRange(min=1.0, max=5.0, 
        message="Dozwolona ocena z przedziału 1.0 - 5.0")],
        render_kw={"step": "0.5"})
    comment = StringField('Komentarz', validators=[Optional(),\
        Length(0, 4000, message="Komentarz nie może mieć więcej, niż 4000 znaków"),],\
            widget=TextArea())
    submit = SubmitField('Zapisz')
    submit.label = None

