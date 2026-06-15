from database import get_db
from werkzeug.security import check_password_hash, generate_password_hash


def serialize_user(row):
    return {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "tipo": row["tipo"],
        "criado_em": row["criado_em"],
    }


def list_users():
    rows = get_db().execute("SELECT * FROM usuarios ORDER BY id").fetchall()
    return [serialize_user(row) for row in rows]


def find_user(user_id):
    row = get_db().execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    return serialize_user(row) if row else None


def create_user(nome, email, senha, tipo="cliente"):
    cursor = get_db().execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome, email, generate_password_hash(senha), tipo),
    )
    get_db().commit()
    return cursor.lastrowid


def authenticate(email, senha):
    row = get_db().execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
    if not row or not check_password_hash(row["senha"], senha):
        return None
    return serialize_user(row)
