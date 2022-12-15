from flask import jsonify, request, url_for, current_app
from sqlalchemy.sql import text

from ..models import GasStation
from ..sql import sql
from . import api


@api.route('/gas_stations/')
def get_gas_stations():
    page = request.args.get('page', 1, type=int)
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    radius = request.args.get('radius', type=int)
    per_page = request.args.get('per_page', type=int)
    if not per_page:
        per_page = current_app.config['STATIONS_PER_PAGE']
    prev, next = None, None

    if lat and lon and radius:
        text_sql = text(sql.select_gas_stations_with_distance)
        text_sql = text_sql.columns(GasStation.id, GasStation.name, GasStation.lat,
            GasStation.lon, GasStation.distance)
        text_sql = text_sql.select().limit(per_page).offset(per_page * (page-1))
        query = GasStation.query.from_statement(text_sql)
        stations = query.params(lat=lat, lon=lon, radius=radius).all()
        total = len(stations)

    else:
        query = GasStation.query
        pagination = query.order_by(GasStation.id).paginate(
                page=page, per_page=per_page,
                error_out=False)
        stations = pagination.items

        if pagination.has_prev:
            prev = url_for('api.get_gas_stations', page=page-1)
        if pagination.has_next:
            next = url_for('api.get_gas_stations', page=page+1)
        total = pagination.total

    return jsonify({
        'gas_stations': [station.to_json() for station in stations],
        'prev': prev,
        'next': next,
        'count': total
    })

@api.route('/gas_stations/<int:id>')
def get_gas_station(id):
    station = GasStation.query.get_or_404(id)
    json = station.to_json()
    json["fuels"] = [fuel.to_json() for fuel in station.fuels]
    return jsonify(json)
