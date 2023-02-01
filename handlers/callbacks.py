from config import *
from utils import *
from .order import start_order, close_order, cancel_order, reject_order
from .vendor import start_vendor


@bot.callback_query_handler(
    func=lambda c: c.data in ["order", "courier", "done", "reject", "cancel"]
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

        if order['vendor'] == call.from_user.username or call.from_user.id == ADMIN:
            # Close order
            close_order(call)

        else:
            pass

    elif call.data == "reject":
        # If Order Validated By Admin

        order = db_client.get_order_by_msg_id(call.message.id)

        if call.from_user.id == ADMIN or call.from_user.username == order['vendor']:
            # Reject order
            reject_order(call)

        else:
            pass

    elif call.data == "cancel":
        # If Order Validated By Admin

        order = db_client.get_order(call.from_user.username)

        if call.from_user.id == ADMIN or call.from_user.username == order['buyer']:
            # Close order
            cancel_order(order['msg_id'])

            bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            pass

    else:
        pass
