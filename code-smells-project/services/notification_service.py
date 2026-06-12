def notify_order_created(order_id, user_id):
    print(f"NOTIFICAÇÃO: Pedido {order_id} criado para usuario {user_id}")


def notify_order_status(order_id, status):
    if status == "aprovado":
        print(f"NOTIFICAÇÃO: Pedido {order_id} foi aprovado. Preparar envio.")
    elif status == "cancelado":
        print(f"NOTIFICAÇÃO: Pedido {order_id} cancelado. Avaliar devolução de estoque.")
