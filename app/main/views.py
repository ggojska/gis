from datetime import datetime
import requests
import json

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user

from . import main
from .. import db
from ..models import GasStation, Car, Comment, fuels_lookup, db
from .forms import CarForm, CommentForm
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


@main.route('/gas_stations/', methods=['GET'])
def gas_station_search():
    api_request = requests.get(request.url_root + url_for('api.get_gas_stations'), params=request.args)
    response = json.loads(api_request.text)
    prev, next, count = response.get("prev"), response.get("next"), response.get("count")
    stations = response.get("gas_stations")
    return render_template('_gas_station_search_result.html', stations=stations,\
        prev=prev, next=next, count=count)


@main.route('/gas_stations/<int:id>/popup', methods=['GET'])
def gas_station_popup(id):
    station = GasStation.query.get(id)
    if not station:
         return page_not_found()
    return render_template('_gas_station_popup.html', station=station)


@main.route('/gas_stations/<int:id>/comments', methods=['GET'])
def get_comments(id):
    station = GasStation.query.get(id)
    if not station:
         return page_not_found()
    form = CommentForm()
    return render_template('_gas_station_big_popup.html', station=station, form=form)


@main.route('/gas_stations/<int:id>/comments', methods=['POST'])
@login_required
def add_comment(id):
    station = GasStation.query.get(id)
    if not station:
         return page_not_found()
    form = CommentForm()
    try:
        new_comment = Comment(rate=form.rate.data,
                    comment=form.comment.data,
                    gas_station_id=station.id,
                    created_at=datetime.now(),
                    user=current_user)
        db.session.add(new_comment)
        db.session.commit()
        station = GasStation.query.get(id)
    except Exception as e:
        print(e)
        flash(e)
    return render_template('_gas_station_big_popup.html', station=station, form=form)


@main.route('/gas_stations/<int:gas_station_id>/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(gas_station_id, comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        flash('brak takiego komentarza')
    if current_user != comment.user:
        flash('nie można usunąc nieswojego komentarza')
    station_id = comment.gas_station_id
    db.session.delete(comment)
    db.session.commit()
    station = GasStation.query.get(station_id)
    flash('usunięto komentarz')
    return render_template('_gas_station_big_popup.html', station=station, form=CommentForm())


@main.route('/searchbox', methods=['GET'])
def get_searchbox():
    fuels = db.session.execute(fuels_lookup).fetchall()
    fuels = [f[0] for f in fuels]
    return render_template('_searchbox.html', fuels=fuels)
