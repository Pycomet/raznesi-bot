from config import *
from utils import *
from models import Order


@bot.message_handler(commands=['order'])
def start_order(msg):
    "Start order creation"
    bot.send_chat_action(msg.from_user.id, "typing")

    if hasattr(msg, "message_id") and msg.chat.type != 'group':
        bot.delete_message(msg.chat.id, msg.message_id)

    question = bot.send_message(
        msg.chat.id,
        f"Welcome back {msg.from_user.first_name}, \n\nWhat would like to order today? \nE.g Flarey sky ",
        parse_mode="html"
    )
    bot.register_next_step_handler(question, add_item)


def add_item(msg):
    "Adding Item"
    item_name = msg.text
    bot.send_chat_action(msg.from_user.id, "typing")

    # Send Order Message & Create Order
    order_msg = bot.send_message(
        CHAT_ID,
        f"<b>New Order Being Created By @{msg.from_user.id}.</b>",
        parse_mode="html",
    )
    order = Order(
        buyer=msg.from_user.id,
        seller="",
        msg_id=order_msg.message_id,
        item=item_name,
        address="",
        created_at=datetime.now().isoformat()
    )
    res = db_client.create_update_order(order=order)
    print(res)

    # Continue process
    bot.send_chat_action(msg.from_user.id, "typing")

    question = bot.send_message(
        msg.from_user.id,
        f"What is the pickup location for this order? ",
        parse_mode="html"
    )
    bot.register_next_step_handler(question, add_pickup)


def add_pickup(msg):
    "Add pickup spot"
    address = msg.text

    order = db_client.get_order(id=msg.from_user.id)

    if order is None:

        bot.send_message(
            msg.from_user.id,
            "Your do not have an open order. Please start a new order by clicking /order"
        )

    else:
        newOrder = Order(
            buyer=msg.from_user.id,
            seller="",
            msg_id=order['msg_id'],
            item=order['item'],
            address=address,
            status="created",
            created_at=order['created_at']
        )

        # Update order
        res = db_client.create_update_order(order=newOrder)

        bot.edit_message_text(
            chat_id=CHAT_ID,
            message_id=order['msg_id'],
            text=f"<b>Order Created By @{newOrder.buyer}</b> \nItem: <b>{newOrder.item}</b> \nPickup at: <b>{newOrder.address}</b>",
            parse_mode="html",
        )

        bot.send_message(
            msg.from_user.id,
            "Order Created! Pleae check main chat to confirm your order"
        )
