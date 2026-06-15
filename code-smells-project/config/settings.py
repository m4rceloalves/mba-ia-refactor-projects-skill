import os

DATABASE_PATH = os.getenv("DATABASE_PATH", "loja.db")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-secret")
DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))
ENABLE_ADMIN_TOOLS = os.getenv("ENABLE_ADMIN_TOOLS", "false").lower() == "true"

VALID_CATEGORIES = {"informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"}
VALID_ORDER_STATUSES = {"pendente", "aprovado", "enviado", "entregue", "cancelado"}
