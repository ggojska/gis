from math import ceil

from flask import jsonify, request, url_for, current_app
from sqlalchemy.sql import text, func, select, column

from ..models import GasStation, Fuel, db
from ..sql import sql
from .errors import bad_request, not_found
from . import api

class GasStationParams:
    lat: float
    lon: float
    radius: float
    page: int
    per_page: int
    name: str
    fuel: str
    min_price: float
    max_price: float
    min_rate: float
    max_rate: float
    sort_by: str
    sort_direction: str

    def __init__(self) -> None:
        pass

    def validate_request(self):
        if self.radius and not self.lat and not self.lon:
            return "when radius is given, lat and lon must be given"
        if self.radius and not self.lat:
            return "when radius is given, lat must be given"
        if self.radius and not self.lon:
            return "when radius is given, lon must be given"
        if (self.lat or self.lon) and not self.radius:
            return "when lat or lon are given, radius must be given"
        if not self.fuel and (self.min_price or self. max_price):
            return "fuel must be given if price is given"

        if self.sort_by:
            if not self.sort_by in ["distance", "price", "average_rate"]:
                return f"not supported sort by field: {self.sort_by}"
            elif self.sort_by == "distance" and (not self.lat or not self.lon or not self.radius):
                return "in order to sort by distance, lat, lon and radius parameters must be given"
            elif self.sort_by == "price" and not self.fuel:
                return "cannot sort by price when fuel is not given"

        if self.sort_direction:
            if not self.sort_direction in ["asc", "desc"]:
                return f"unknown sort direction: {self.sort_direction}"

    def from_request(self, request):
        self.page =request.get('page', 1, type=int)
        self.lat =request.get('lat', type=float)
        self.lon =request.get('lon', type=float)
        self.radius =request.get('radius', type=int)
        self.per_page =request.get('per_page', type=int)
        if not self.per_page:
            self.per_page = current_app.config['STATIONS_PER_PAGE']
        self.name = request.get("name")
        if self.name:
            self.name = self.name.lower()
            self.name_search = f"%{self.name.lower()}%"
        self.fuel = request.get("fuel")
        if self.fuel:
            self.fuel = self.fuel.lower()
            self.fuel_search = f"%{self.fuel.lower()}%"
        self.min_price = request.get("min_price", type=float)
        self.max_price = request.get("max_price", type=float)
        self.min_rate = request.get("min_rate", type=float)
        self.max_rate = request.get("max_rate", type=float)
        self.sort_by = request.get("sort_by")
        self.sort_direction = request.get("sort_direction")

    def to_dict(self):
        dict = {
            "page": self.page,
            "lat": self.lat,
            "lon": self.lon,
            "radius": self.radius,
            "page": self.per_page,
            "name": self.name,
            "fuel": self.fuel,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "min_rate": self.min_rate,
            "max_rate": self.max_rate,
            "sort_by": self.sort_by,
            "sort_direction": self.sort_direction
        }
        return dict


@api.route('/gas_stations/')
def get_gas_stations():
    params = GasStationParams()
    params.from_request(request.args)
    validation_result = params.validate_request()
    if validation_result: return bad_request(validation_result)

    query, sort_by_column = build_query(params)
    if not get_sort_by_column(params.sort_by,params. sort_direction) is None:
        sort_by_column = get_sort_by_column(params.sort_by, params.sort_direction)
    query_ordered = query.order_by(sort_by_column)

    offset = params.per_page * (params.page-1)
    records = query_ordered.limit(params.per_page).offset(offset).distinct()
    total = query_ordered.distinct(GasStation.id).count()

    next, prev = None, None
    if params.page > 1:
        prev = url_for('api.get_gas_stations', page=params.page-1, per_page=params.per_page,\
            name=params.name, lat=params.lat, lon=params.lon, radius=params.radius,\
            fuel=params.fuel, min_price=params.min_price, max_price=params.max_price,\
            min_rate=params.min_rate, max_rate=params.max_rate,\
            sort_by=params.sort_by, sort_direction=params.sort_direction)
    if ceil(total/params.per_page) > params.page:
        next = url_for('api.get_gas_stations', page=params.page+1, per_page=params.per_page,\
            name=params.name, lat=params.lat, lon=params.lon, radius=params.radius,\
            fuel=params.fuel, min_price=params.min_price, max_price=params.max_price,\
            min_rate=params.min_rate, max_rate=params.max_rate,\
            sort_by=params.sort_by, sort_direction=params.sort_direction)

    stations_list = []
    if records.count() > 0:
        for record in records:
            distance = None
            if type(record) == GasStation:
                station = record
            else:
                station = record[0]
                distance = record[1]

            d = station.to_json()
            d["distance"] = distance
            if hasattr(params, 'fuel_search'):
                for fuel in station.fuels:
                    if fuel.name.lower() == params.fuel:
                        d["fuel"] = fuel.to_json()
                        break

            stations_list.append(d)

    return jsonify({
        'gas_stations': stations_list,
        'prev': prev,
        'next': next,
        'count': total
    })

def build_query(params):
    query = db.session.query(GasStation).outerjoin(GasStation.fuels)
    sort_by_column = GasStation.id

    if params.name:
        query = query.filter(func.lower(GasStation.name).like(params.name_search))
    if params.fuel:
        query = query.filter(func.lower(Fuel.name).like(params.fuel_search))

    if (params.min_price or params.max_price):
        if params. min_price and not params.max_price:
            query = query.filter(Fuel.price >= params.min_price)
        elif params.max_price and not params. min_price:
            query = query.filter(Fuel.price <= params.max_price)
        else:
            query = query.filter(Fuel.price >= params.min_price).\
                filter(Fuel.price <= params.max_price)

    if (params.min_rate or params.max_rate):
        if params.min_rate and not params.max_rate:
            query = query.filter(GasStation.average_rate >= params.min_rate)
        elif params.max_rate and not params.min_rate:
            query = query.filter(GasStation.average_rate <= params.max_rate)
        else:
            query = query.filter(GasStation.average_rate >= params.min_rate).\
                filter(GasStation.average_rate <= params.max_rate)

    if params.lat and params.lon and params.radius:
        text_sql = text(sql.select_gas_stations_with_distance.replace(":lon", str(params.lon))\
            .replace(":lat", str(params.lat)))
        cte = select([column('id'), column('harvesine')], use_labels=True).select_from(text_sql)\
            .cte("cte")
        query = query.add_columns(column('harvesine').label("harvesine"))\
                .join(cte, cte.columns["id"] == GasStation.id)\
                .filter(column('harvesine') < params.radius)
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
