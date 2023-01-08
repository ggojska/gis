from math import ceil

from flask import jsonify, request, url_for, current_app
from sqlalchemy.sql import text, func, select, column

from ..models import GasStation, Fuel, Comment, db
from ..sql import sql
from .errors import bad_request, not_found
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
    next, prev = None, None
    name, fuel, price_range, sort_by, sort_direction = None, None, None, None, None

    validation_result = validate_request(lat, lon, radius, {})
    if validation_result: return bad_request(validation_result)

    if request.content_type == "application/json":
        search_params = request.get_json()
        if search_params:
            validation_result = validate_request(lat, lon, radius, search_params)
            if validation_result: return bad_request(validation_result)
            name, fuel, price_range, sort_by, sort_direction = get_search_params(search_params)

    query, sort_by_column = build_query(lat, lon, radius, name, fuel, price_range)
    if not get_sort_by_column(sort_by, sort_direction) is None:
        sort_by_column = get_sort_by_column(sort_by, sort_direction)
    query_ordered = query.order_by(sort_by_column)

    offset = per_page * (page-1)
    stations = query_ordered.limit(per_page).offset(offset).distinct()
    total = query_ordered.distinct(GasStation.id).count()

    if page > 1:
        prev = url_for('api.get_gas_stations', page=page-1)
    if ceil(total/per_page) > page:
        next = url_for('api.get_gas_stations', page=page+1)

    stations_list = []
    if stations.count() > 0:
        if type(stations[0]) == GasStation:
            stations_list = [station.to_json() for station in stations]
        else:
            for station in stations:
                d = station[0].to_json()
                d["distance"] = station[1]
                stations_list.append(d)

    return jsonify({
        'gas_stations': stations_list,
        'prev': prev,
        'next': next,
        'count': total
    })


def validate_request(lat, lon, radius, search_params):
    name = search_params.get("name")
    fuel = search_params.get("fuel")
    price_range = search_params.get("price_range")

    if radius and not lat and not lon:
        return "when radius is given, lat and lon must be given"
    if radius and not lat:
        return "when radius is given, lat must be given"
    if radius and not lon:
        return "when radius is given, lon must be given"
    if (lat or lon) and not radius:
        return "when lat or lon are given, radius must be given"

    if price_range:
        if len(price_range) > 2:
            return "price range can contain up to two values"

    if not fuel and price_range:
        return "fuel must be given if price is given"

    sort_by = search_params.get("sort_by")
    if sort_by:
        if not sort_by in ["distance", "price", "average_rate"]:
            return f"not supported sort by field: {sort_by}"
        elif sort_by == "distance" and (not lat or not lon or not radius):
            return "in order to sort by distance, lat, lon and radius parameters must be given"
        elif sort_by == "price" and not fuel:
            return "cannot sort by price when fuel is not given"

    sort_direction = search_params.get("sort_direction")
    if sort_direction:
        if not sort_direction in ["asc", "desc"]:
            return f"unknown sort direction: {sort_direction}"

def get_search_params(search_params):
    name = search_params.get("name")
    if name: name = f"%{name.lower()}%"
    fuel = search_params.get("fuel")
    if fuel: fuel = f"%{fuel.lower()}%"
    price_range = search_params.get("price_range")
    sort_by = search_params.get("sort_by")
    sort_direction = search_params.get("sort_direction")
    return name, fuel, price_range, sort_by, sort_direction

def build_query(lat, lon, radius, name, fuel, price_range):
    query = db.session.query(GasStation).outerjoin(GasStation.fuels)
    sort_by_column = GasStation.id

    if name:
        query = query.filter(func.lower(GasStation.name).like(name))
    if fuel:
        query = query.filter(func.lower(Fuel.name).like(fuel))
    if price_range:
        print(price_range)
        if price_range[0] and not price_range[1]:
            query = query.filter(Fuel.price >= price_range[0])
        elif price_range[1] and not price_range[0]:
            query = query.filter(Fuel.price <= price_range[1])
        else:
            query = query.filter(Fuel.price >= price_range[0]).filter(Fuel.price <= price_range[1])
    if lat and lon and radius:
        text_sql = text(sql.select_gas_stations_with_distance.replace(":lon", str(lon))\
            .replace(":lat", str(lat)))
        cte = select([column('id'), column('harvesine')], use_labels=True).select_from(text_sql)\
            .cte("cte")
        query = query.add_columns(column('harvesine').label("harvesine"))\
                .join(cte, cte.columns["id"] == GasStation.id)\
                .filter(column('harvesine') < radius)
        sort_by_column = column('harvesine').asc()

    return query, sort_by_column

def get_sort_by_column(sort_by, sort_direction):
    sort_by_column = None
    if sort_by:
        if sort_by == "price":
            if sort_direction == "desc":
                sort_by_column = Fuel.price.desc()
            else:
                sort_by_column = Fuel.price.asc()
        if sort_by == "distance":
            if sort_direction == "desc":
                sort_by_column = column('harvesine').desc()
            else:
                sort_by_column= column('harvesine').asc()
        if sort_by == "average_rate":
            if sort_direction == "desc":
                sort_by_column = GasStation.average_rate.desc()
            else:
                sort_by_column = GasStation.average_rate.asc()
    return sort_by_column


@api.route('/gas_stations/<int:id>')
def get_gas_station(id):
    station = GasStation.query.get(id)
    if not station:
         return not_found(f'stacja o id {id} nie istnieje')
    json = station.to_json()
    json["fuels"] = [fuel.to_json() for fuel in station.fuels]
    json["comments"] = [comment.to_json() for comment in station.comments]
    return jsonify(json)
