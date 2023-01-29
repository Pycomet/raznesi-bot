from config import *
from utils import *
from .order import start_order, close_order, cancel_order
from .vendor import start_vendor


@bot.callback_query_handler(
    func=lambda c: c.data in ["order", "courier", "done", "cancel"]
)
def button_callback_answer(call):
    """
    Button Response
    """
    bot.send_chat_action(call.from_user.id, "typing")

    if call.data == "order":
        # Taking In New Order
        start_order(call)

    elif call.data == "courier":
        # If Order Taken By Vendor
        start_vendor(call)

    elif call.data == "done":
        # If Order Validated By Admin

        order = db_client.get_order_by_msg_id(call.message.id)

        if order['buyer'] == call.from_user.username or call.from_user.id == ADMIN:
            # Close order
            close_order(call)

        else:
            pass

    elif call.data == "cancel":
        # If Order Validated By Admin

        order = db_client.get_order_by_msg_id(call.message.id)

        if call.from_user.id == ADMIN:
            # Close order
            cancel_order(call)

        else:
            pass

    else:
        pass
