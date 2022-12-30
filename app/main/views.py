from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from . import main
from .. import db
from ..models import GasStation, Car, fuels_lookup, db
from .forms import CarForm
from .errors import page_not_found


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

@main.route('/cars/<int:id>/delete', methods=['POST'])
@login_required
def delete_car(id):
    car = Car.query.get(id)
    if not car:
        flash('brak takiego samochodu')
        return redirect(url_for('main.my_account'))
    if current_user != car.user:
        flash('nie można usunąc nieswojego samochodu')
        return redirect(url_for('main.my_account'))
    db.session.delete(car)
    db.session.commit()
    flash('usunięto samochód')
    return redirect(url_for('main.my_account'))

@main.route('/gas_stations/<int:id>/popup', methods=['GET'])
def gas_station_popup(id):
    station = GasStation.query.get(id)
    if not station:
         return page_not_found()
    return render_template('_gas_station_popup.html', station=station)

@main.route('/gas_stations/<int:id>/bigpopup', methods=['GET'])
def gas_station_big_popup(id):
    station = GasStation.query.get(id)
    if not station:
         return page_not_found()
    return render_template('_gas_station_big_popup.html', station=station)
