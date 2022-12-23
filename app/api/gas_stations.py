from math import ceil

from flask import jsonify, request, url_for, current_app
from sqlalchemy.sql import text, func, select, column

from ..models import GasStation, Fuel, db
from ..sql import sql
from . import api, errors


@api.route('/gas_stations/')
def get_gas_stations():
    page = request.args.get('page', 1, type=int)
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    radius = request.args.get('radius', type=int)
    name = request.args.get('name', type=str)
    if name:
        name = f"%{name.lower()}%"
    fuel = request.args.get('fuel', type=str)
    if fuel:
        fuel = f"%{fuel.lower()}%"
    per_page = request.args.get('per_page', type=int)
    if not per_page:
        per_page = current_app.config['STATIONS_PER_PAGE']
    next, prev = None, None

    query = db.session.query(GasStation).outerjoin(GasStation.fuels)

    if name:
        query = query.filter(func.lower(GasStation.name).like(name))

    if fuel:
        query = query.filter(func.lower(Fuel.name).like(fuel))

    if lat and lon and radius:
        text_sql = text(sql.select_gas_stations_with_distance.replace(":lon", str(lon))\
            .replace(":lat", str(lat)))
        cte = select([column('id'), column('harvesine')], use_labels=True).select_from(text_sql)\
            .cte("cte")
        query_ordered = query.join(cte, cte.columns["id"] == GasStation.id)\
                .filter(column('harvesine') < radius)\
                .order_by(column('harvesine').asc())
    else:
        query_ordered = query.order_by(GasStation.id)

    offset = per_page * (page-1)
    stations = query_ordered.limit(per_page).offset(offset).distinct()
    total = query_ordered.distinct(GasStation.id).count()
    
    if page > 1:
        prev = url_for('api.get_gas_stations', page=page-1)
    if ceil(total/per_page) > page:
        next = url_for('api.get_gas_stations', page=page+1)

    return jsonify({
        'gas_stations': [station.to_json() for station in stations],
        'prev': prev,
        'next': next,
        'count': total
    })

@api.route('/gas_stations/<int:id>')
def get_gas_station(id):
    station = GasStation.query.get(id)
    if not station:
         return errors.not_found(f'stacja o id {id} nie istnieje')
    json = station.to_json()
    json["fuels"] = [fuel.to_json() for fuel in station.fuels]
    return jsonify(json)
