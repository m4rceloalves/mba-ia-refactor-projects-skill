from flask import jsonify, request

from services import category_service


def get_categories():
    return jsonify(category_service.list_categories()), 200


def create_category():
    return jsonify(category_service.create_category(request.get_json())), 201


def update_category(cat_id):
    return jsonify(category_service.update_category(cat_id, request.get_json())), 200


def delete_category(cat_id):
    category_service.delete_category(cat_id)
    return jsonify({'message': 'Categoria deletada'}), 200
