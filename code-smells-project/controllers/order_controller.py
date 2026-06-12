from flask import jsonify, request

from models import order_model
from services.notification_service import notify_order_created, notify_order_status
from services.validation_service import validate_order_payload, validate_order_status


def criar_pedido():
    usuario_id, itens = validate_order_payload(request.get_json())
    resultado = order_model.create_order(usuario_id, itens)
    if "erro" in resultado:
        return jsonify({"erro": resultado["erro"], "sucesso": False}), 400
    notify_order_created(resultado["pedido_id"], usuario_id)
    return jsonify({
        "dados": resultado,
        "sucesso": True,
        "mensagem": "Pedido criado com sucesso",
    }), 201


def listar_todos_pedidos():
    return jsonify({"dados": order_model.list_orders(), "sucesso": True}), 200


def listar_pedidos_usuario(usuario_id):
    return jsonify({"dados": order_model.list_orders(usuario_id), "sucesso": True}), 200


def atualizar_status_pedido(pedido_id):
    status = validate_order_status((request.get_json() or {}).get("status", ""))
    order_model.update_status(pedido_id, status)
    notify_order_status(pedido_id, status)
    return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200
