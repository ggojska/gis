from flask import render_template
from flask_login import login_required, current_user

from . import main
from .. import db
from ..models import Car, fuels_lookup, db
from .forms import CarForm


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html', mapa=True)

@main.route('/my-account', methods=['GET', 'POST'])
@login_required
def my_account():
    form = CarForm()
    fuels = db.session.execute(fuels_lookup).fetchall()
    form.fuel.choices = [(f[0], f[0]) for f in fuels]
    if form.validate_on_submit():
        car = Car(make=form.make.data,
                    model=form.model.data,
                    combustion=form.combustion.data,
                    fuel=form.fuel.data,
                    user=current_user)
        db.session.add(car)
        db.session.commit()
    return render_template('my_account.html', form=form)
