from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length


class CarForm(FlaskForm):
    make = StringField('Marka', validators=[DataRequired(),
        Length(1, 20, message="Marka samochodu musi być uzupełniona."),])
    model = StringField('Model', validators=[DataRequired(),
        Length(1, 20, message="Model samochodu musi być uzupełniona."),])
    combustion = DecimalField('Spalanie', places=1, validators=[DataRequired(),])
    fuel = SelectField(u'Paliwo', validators=[DataRequired(),])
    submit = SubmitField('Dodaj')
    submit.label = None
