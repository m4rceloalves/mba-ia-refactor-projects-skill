from database import get_db


def sales_report():
    row = get_db().execute(
        """
        SELECT
            COUNT(*) AS total_pedidos,
            COALESCE(SUM(total), 0) AS faturamento,
            SUM(CASE WHEN status = 'pendente' THEN 1 ELSE 0 END) AS pendentes,
            SUM(CASE WHEN status = 'aprovado' THEN 1 ELSE 0 END) AS aprovados,
            SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END) AS cancelados
          FROM pedidos
        """
    ).fetchone()

    faturamento = row["faturamento"] or 0
    desconto = calculate_discount(faturamento)
    total_pedidos = row["total_pedidos"]
    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": round(faturamento, 2),
        "desconto_aplicavel": round(desconto, 2),
        "faturamento_liquido": round(faturamento - desconto, 2),
        "pedidos_pendentes": row["pendentes"] or 0,
        "pedidos_aprovados": row["aprovados"] or 0,
        "pedidos_cancelados": row["cancelados"] or 0,
        "ticket_medio": round(faturamento / total_pedidos, 2) if total_pedidos else 0,
    }


def calculate_discount(revenue):
    if revenue > 10000:
        return revenue * 0.1
    if revenue > 5000:
        return revenue * 0.05
    if revenue > 1000:
        return revenue * 0.02
    return 0
