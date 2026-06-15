from config.settings import VALID_CATEGORIES, VALID_ORDER_STATUSES
from middlewares.error_handler import AppError


def validate_product_payload(data, partial=False):
    if not data:
        raise AppError("Dados inválidos", 400)

    required_fields = {"nome", "preco", "estoque"}
    if not partial:
        missing = required_fields - set(data)
        if missing:
            raise AppError(f"{missing.pop()} é obrigatório", 400)

    payload = {
        "nome": data.get("nome", ""),
        "descricao": data.get("descricao", ""),
        "preco": data.get("preco"),
        "estoque": data.get("estoque"),
        "categoria": data.get("categoria", "geral"),
    }

    if len(payload["nome"]) < 2:
        raise AppError("Nome muito curto", 400)
    if len(payload["nome"]) > 200:
        raise AppError("Nome muito longo", 400)
    if payload["preco"] is None or payload["preco"] < 0:
        raise AppError("Preço não pode ser negativo", 400)
    if payload["estoque"] is None or payload["estoque"] < 0:
        raise AppError("Estoque não pode ser negativo", 400)
    if payload["categoria"] not in VALID_CATEGORIES:
        raise AppError(f"Categoria inválida. Válidas: {sorted(VALID_CATEGORIES)}", 400)
    return payload


def validate_order_payload(data):
    if not data:
        raise AppError("Dados inválidos", 400)
    usuario_id = data.get("usuario_id")
    itens = data.get("itens", [])
    if not usuario_id:
        raise AppError("Usuario ID é obrigatório", 400)
    if not itens:
        raise AppError("Pedido deve ter pelo menos 1 item", 400)
    return usuario_id, itens


def validate_order_status(status):
    if status not in VALID_ORDER_STATUSES:
        raise AppError("Status inválido", 400)
    return status
