from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length

from ..models import Car


class CarForm(FlaskForm):
    make = StringField('Marka', validators=[DataRequired(),
        Length(1, 20, message="Marka samochodu musi być uzupełniona."),])
    model = StringField('Model', validators=[DataRequired(),
        Length(1, 20, message="Model samochodu musi być uzupełniona."),])
    combustion = DecimalField('Spalanie', places=1, validators=[DataRequired(),])
    fuel = StringField('Paliwo', validators=[DataRequired(),
        Length(1, 10, message="Paliwo samochodu musi być uzupełnione."),])
    submit = SubmitField('Dodaj')
    submit.label = None
