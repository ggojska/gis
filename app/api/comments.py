from datetime import datetime

from flask import jsonify, request, url_for, current_app, g

from ..models import GasStation, Comment, db
from . import api, errors


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


@api.route('/comments/<int:id>')
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())


@api.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    db.session.remove(comment)
    db.session.commit()
    response = jsonify({"message": "Resource successfully deleted"})
    response.status_code = 201
    return response


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


@api.route('/gas_stations/<int:id>/comments', methods=['POST'])
def post_new_comment(id):
    station = GasStation.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.user = g.current_user
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_json()), 201, \
        {'Location': url_for('api.get_comment', id=comment.id)}


@api.route('/comments/<int:id>', methods=['PUT'])
def update_comment(id):
    comment = Comment.query.get_or_404(id)
    if g.current_user != comment.user:
        return errors.forbidden('Nie można edytować komentarzy innych użytkowników')

    new_comment = Comment.from_json(request.json)
    comment.comment = new_comment.comment
    comment.rate = new_comment.rate
    comment.updated_at = datetime.now()
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_json())