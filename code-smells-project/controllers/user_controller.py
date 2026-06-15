from flask import jsonify, request

from middlewares.error_handler import AppError
from models import user_model


def listar_usuarios():
    return jsonify({"dados": user_model.list_users(), "sucesso": True}), 200


def buscar_usuario(id):
    usuario = user_model.find_user(id)
    if not usuario:
        raise AppError("Usuário não encontrado", 404)
    return jsonify({"dados": usuario, "sucesso": True}), 200


def criar_usuario():
    dados = request.get_json()
    if not dados:
        raise AppError("Dados inválidos", 400)
    nome = dados.get("nome", "")
    email = dados.get("email", "")
    senha = dados.get("senha", "")
    if not nome or not email or not senha:
        raise AppError("Nome, email e senha são obrigatórios", 400)
    user_id = user_model.create_user(nome, email, senha)
    return jsonify({"dados": {"id": user_id}, "sucesso": True}), 201


def login():
    dados = request.get_json()
    if not dados:
        raise AppError("Dados inválidos", 400)
    email = dados.get("email", "")
    senha = dados.get("senha", "")
    if not email or not senha:
        raise AppError("Email e senha são obrigatórios", 400)
    usuario = user_model.authenticate(email, senha)
    if not usuario:
        return jsonify({"erro": "Email ou senha inválidos", "sucesso": False}), 401
    return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200
