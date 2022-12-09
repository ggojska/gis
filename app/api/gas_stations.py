from flask import jsonify, request, g, url_for, current_app


from .. import db
from ..models import GasStation
from . import api


@api.route('/gas_stations/')
def get_gas_stations():
    page = request.args.get('page', 1, type=int)
    pagination = GasStation.query.paginate(
        page=page, per_page=current_app.config['STATIONS_PER_PAGE'],
        error_out=False)
    stations = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_gas_stations', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_gas_stations', page=page+1)
    return jsonify({
        'gas_stations': [station.to_json() for station in stations],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
