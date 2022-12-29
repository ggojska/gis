from flask import render_template, flash
from flask_login import login_required

from . import main
from .. import db
from ..models import Car
from .forms import CarForm


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html', mapa=True)

@main.route('/my-account', methods=['GET', 'POST'])
@login_required
def my_account():
    form = CarForm()
    if form.validate_on_submit():
        car = Car(make=form.make.data,
                    model=form.model.data,
                    combustion=form.combustion.data,
                    fuel=form.fuel.data)
        db.session.add(car)
        db.session.commit()
    return render_template('my_account.html', form=form)
