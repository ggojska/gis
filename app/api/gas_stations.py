from flask import jsonify, request, url_for, current_app
from sqlalchemy.sql import text

from ..models import GasStation, db
from ..sql import sql
from . import api


@api.route('/gas_stations/')
def get_gas_stations():
    page = request.args.get('page', 1, type=int)
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    radius = request.args.get('radius', type=int)
    prev, next = None, None

    if lat and lon and radius:
        query = GasStation.query.from_statement(text(sql.select_gas_stations_with_distance)).\
            params(lat=lat, lon=lon, radius=radius).all()
        stations = query
        total = len(stations)

    else:
        query = GasStation.query
        pagination = query.paginate(
                page=page, per_page=current_app.config['STATIONS_PER_PAGE'],
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
