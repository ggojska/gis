from datetime import datetime

from flask import jsonify, request, url_for, current_app, g

from ..models import User, Car, db
from . import api, errors


@api.route('/cars/<int:id>')
def get_car(id):
    car = Car.query.get(id)
    if not car:
         return errors.not_found(f'nie znaleziono samochodu')
    return jsonify(car.to_json())


@api.route('/users/<int:id>/cars')
def get_user_cars(id):
    user = User.query.get(id)
    if not user:
         return errors.not_found(f'użytkownik o id {id} nie istnieje')

    return jsonify({
        'cars': [car.to_json() for car in user.cars],
    })


@api.route('/users/<int:id>/cars', methods=['POST'])
def add_new_car(id):
    if not g.get("current_user"):
        return errors.unauthorized("operacja dozwolona tylko dla zalogowanego użytkownika")

    user = User.query.get(id)
    if not user:
         return errors.not_found(f'użytkownik o id {id} nie istnieje')
    
    car = Car.from_json(request.json)
    car.user_id = id
    db.session.add(car)
    db.session.commit()

    return jsonify(car.to_json()), 201, \
        {'Location': url_for('api.get_car', id=car.id)}


@api.route('/cars/<int:id>', methods=['PUT'])
def update_car(id):
    if not g.get("current_user"):
        return errors.unauthorized("operacja dozwolona tylko dla zalogowanego użytkownika")

    car = Car.query.get(id)
    if not car:
         return errors.not_found(f'nie znaleziono samochodu')

    if g.current_user != car.user:
        return errors.forbidden('nie można edytować samochodów innych użytkowników')

    new_car = Car.from_json(request.json)
    car.model = new_car.model
    car.make = new_car.make
    car.combustion = new_car.combustion
    car.fuel = new_car.fuel
    db.session.add(car)
    db.session.commit()

    return jsonify(car.to_json())
