from datetime import datetime

from flask import jsonify, request, url_for, g

from ..models import GasStation, Comment, db
from . import api, errors


@api.route('/comments/<int:id>')
def get_comment(id):
    comment = Comment.query.get(id)
    if not comment:
         return errors.not_found(f'nie znaleziono komentarza')
    return jsonify(comment.to_json())


@api.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    if not g.get("current_user"):
        return errors.unauthorized("operacja dozwolona tylko dla zalogowanego użytkownika")

    if g.current_user != comment.user:
        return errors.forbidden('nie można usuwać komentarzy innych użytkowników')

    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    response = jsonify({"message": "resource successfully deleted"})
    response.status_code = 201
    return response


@api.route('/gas_stations/<int:id>/comments', methods=['POST'])
def post_new_comment(id):
    if not g.get("current_user"):
        return errors.unauthorized("operacja dozwolona tylko dla zalogowanego użytkownika")

    station = GasStation.query.get(id)
    if not station:
         return errors.not_found(f'stacja o id {id} nie istnieje')

    comment = Comment.from_json(request.json)
    comment.user = g.current_user
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_json()), 201, \
        {'Location': url_for('api.get_comment', id=comment.id)}


@api.route('/comments/<int:id>', methods=['PUT'])
def update_comment(id):
    if not g.get("current_user"):
        return errors.unauthorized("operacja dozwolona tylko dla zalogowanego użytkownika")

    comment = Comment.query.get(id)
    if not comment:
         return errors.not_found(f'nie znaleziono komentarza')

    if g.current_user != comment.user:
        return errors.forbidden('nie można edytować komentarzy innych użytkowników')

    new_comment = Comment.from_json(request.json)
    comment.comment = new_comment.comment
    comment.rate = new_comment.rate
    comment.updated_at = datetime.now()
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_json())