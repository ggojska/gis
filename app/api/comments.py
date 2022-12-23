from flask import jsonify, request, url_for, current_app

from ..models import GasStation, Comment
from ..sql import sql
from . import api


@api.route('/comments/')
def get_comments():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', type=int)
    if not per_page:
        per_page = current_app.config['STATIONS_PER_PAGE']

    pagination = Comment.query.order_by(Comment.created_at.desc()).paginate(
        page=page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    prev, next = None, None

    if pagination.has_prev:
        prev = url_for('api.get_comments', page=page-1)

    if pagination.has_next:
        next = url_for('api.get_comments', page=page+1)

    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/gas_stations/<int:id>/comments')
def get_gas_station_comments(id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', type=int)
    if not per_page:
        per_page = current_app.config['STATIONS_PER_PAGE']

    station = GasStation.query.get_or_404(id)
    pagination = station.comments.order_by(Comment.created_at.asc()).paginate(
        page=page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    prev, next = None, None

    if pagination.has_prev:
        prev = url_for('api.get_post_comments', id=id, page=page-1)

    if pagination.has_next:
        next = url_for('api.get_post_comments', id=id, page=page+1)

    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
