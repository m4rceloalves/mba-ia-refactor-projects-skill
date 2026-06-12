from flask import jsonify, request

from middlewares.error_handler import AppError
from models import product_model
from services.validation_service import validate_product_payload


def listar_produtos():
    produtos = product_model.list_products()
    return jsonify({"dados": produtos, "sucesso": True}), 200


def buscar_produto(id):
    produto = product_model.find_product(id)
    if not produto:
        raise AppError("Produto não encontrado", 404)
    return jsonify({"dados": produto, "sucesso": True}), 200


def criar_produto():
    payload = validate_product_payload(request.get_json())
    product_id = product_model.create_product(payload)
    return jsonify({"dados": {"id": product_id}, "sucesso": True, "mensagem": "Produto criado"}), 201


def atualizar_produto(id):
    if not product_model.find_product(id):
        raise AppError("Produto não encontrado", 404)
    payload = validate_product_payload(request.get_json())
    product_model.update_product(id, payload)
    return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200


def deletar_produto(id):
    if not product_model.find_product(id):
        raise AppError("Produto não encontrado", 404)
    product_model.delete_product(id)
    return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200


def buscar_produtos():
    min_price = request.args.get("preco_min", type=float)
    max_price = request.args.get("preco_max", type=float)
    resultados = product_model.search_products(
        term=request.args.get("q", ""),
        category=request.args.get("categoria"),
        min_price=min_price,
        max_price=max_price,
    )
    return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200
