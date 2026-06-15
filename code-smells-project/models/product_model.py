from database import get_db


def serialize_product(row):
    return {
        "id": row["id"],
        "nome": row["nome"],
        "descricao": row["descricao"],
        "preco": row["preco"],
        "estoque": row["estoque"],
        "categoria": row["categoria"],
        "ativo": row["ativo"],
        "criado_em": row["criado_em"],
    }


def list_products():
    rows = get_db().execute("SELECT * FROM produtos ORDER BY id").fetchall()
    return [serialize_product(row) for row in rows]


def find_product(product_id):
    row = get_db().execute("SELECT * FROM produtos WHERE id = ?", (product_id,)).fetchone()
    return serialize_product(row) if row else None


def create_product(data):
    cursor = get_db().execute(
        "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
        (data["nome"], data["descricao"], data["preco"], data["estoque"], data["categoria"]),
    )
    get_db().commit()
    return cursor.lastrowid


def update_product(product_id, data):
    get_db().execute(
        """
        UPDATE produtos
           SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ?
         WHERE id = ?
        """,
        (data["nome"], data["descricao"], data["preco"], data["estoque"], data["categoria"], product_id),
    )
    get_db().commit()


def delete_product(product_id):
    get_db().execute("DELETE FROM produtos WHERE id = ?", (product_id,))
    get_db().commit()


def search_products(term=None, category=None, min_price=None, max_price=None):
    clauses = []
    params = []

    if term:
        clauses.append("(nome LIKE ? OR descricao LIKE ?)")
        params.extend([f"%{term}%", f"%{term}%"])
    if category:
        clauses.append("categoria = ?")
        params.append(category)
    if min_price is not None:
        clauses.append("preco >= ?")
        params.append(min_price)
    if max_price is not None:
        clauses.append("preco <= ?")
        params.append(max_price)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    rows = get_db().execute(f"SELECT * FROM produtos {where} ORDER BY id", params).fetchall()
    return [serialize_product(row) for row in rows]
