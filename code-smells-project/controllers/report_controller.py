from flask import jsonify

from database import get_db, reset_database
from config.settings import ENABLE_ADMIN_TOOLS
from middlewares.error_handler import AppError
from models import report_model


def relatorio_vendas():
    return jsonify({"dados": report_model.sales_report(), "sucesso": True}), 200


def health_check():
    db = get_db()
    counts = {
        "produtos": db.execute("SELECT COUNT(*) FROM produtos").fetchone()[0],
        "usuarios": db.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0],
        "pedidos": db.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0],
    }
    return jsonify({"status": "ok", "database": "connected", "counts": counts, "versao": "1.0.0"}), 200


def reset_database_admin():
    if not ENABLE_ADMIN_TOOLS:
        raise AppError("Ferramentas administrativas desabilitadas", 403)
    reset_database()
    return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200


def executar_query_admin():
    raise AppError("Execução de SQL arbitrário foi desabilitada", 403)
