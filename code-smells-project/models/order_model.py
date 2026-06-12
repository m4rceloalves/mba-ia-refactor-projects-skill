from database import get_db


def create_order(usuario_id, itens):
    db = get_db()
    total = 0
    products = {}

    for item in itens:
        product_id = item["produto_id"]
        product = db.execute("SELECT * FROM produtos WHERE id = ?", (product_id,)).fetchone()
        if product is None:
            return {"erro": f"Produto {product_id} não encontrado"}
        if product["estoque"] < item["quantidade"]:
            return {"erro": f"Estoque insuficiente para {product['nome']}"}
        products[product_id] = product
        total += product["preco"] * item["quantidade"]

    cursor = db.execute(
        "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, ?, ?)",
        (usuario_id, "pendente", total),
    )
    pedido_id = cursor.lastrowid

    for item in itens:
        product = products[item["produto_id"]]
        db.execute(
            """
            INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
            VALUES (?, ?, ?, ?)
            """,
            (pedido_id, item["produto_id"], item["quantidade"], product["preco"]),
        )
        db.execute(
            "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
            (item["quantidade"], item["produto_id"]),
        )

    db.commit()
    return {"pedido_id": pedido_id, "total": total}


def list_orders(usuario_id=None):
    params = []
    where = ""
    if usuario_id is not None:
        where = "WHERE p.usuario_id = ?"
        params.append(usuario_id)

    orders = get_db().execute(
        f"SELECT p.* FROM pedidos p {where} ORDER BY p.id",
        params,
    ).fetchall()
    if not orders:
        return []

    order_ids = [row["id"] for row in orders]
    placeholders = ",".join("?" for _ in order_ids)
    item_rows = get_db().execute(
        f"""
        SELECT i.pedido_id, i.produto_id, i.quantidade, i.preco_unitario, pr.nome AS produto_nome
          FROM itens_pedido i
          LEFT JOIN produtos pr ON pr.id = i.produto_id
         WHERE i.pedido_id IN ({placeholders})
         ORDER BY i.id
        """,
        order_ids,
    ).fetchall()

    items_by_order = {}
    for item in item_rows:
        items_by_order.setdefault(item["pedido_id"], []).append({
            "produto_id": item["produto_id"],
            "produto_nome": item["produto_nome"] or "Desconhecido",
            "quantidade": item["quantidade"],
            "preco_unitario": item["preco_unitario"],
        })

    return [
        {
            "id": row["id"],
            "usuario_id": row["usuario_id"],
            "status": row["status"],
            "total": row["total"],
            "criado_em": row["criado_em"],
            "itens": items_by_order.get(row["id"], []),
        }
        for row in orders
    ]


def update_status(pedido_id, status):
    get_db().execute("UPDATE pedidos SET status = ? WHERE id = ?", (status, pedido_id))
    get_db().commit()
