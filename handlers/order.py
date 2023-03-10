from config import *
from utils import *
from models import Order


def order_menu():
    "Attached To Order When Created"
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    a = types.InlineKeyboardButton("🙋 Take Order", callback_data="courier")
    keyboard.add(a)
    return keyboard


def cancel_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    a = types.InlineKeyboardButton("❌ Cancel Order", callback_data="cancel")
    keyboard.add(a)
    return keyboard


@bot.message_handler(commands=['order'])
def start_order(msg):
    "Start order creation"
    bot.send_chat_action(msg.from_user.id, "typing")

    if handler_state.get("Requests", False):
        logging.info("Bot is silent")
        bot.send_message(
            msg.from_user.id,
            f"Trenutno nema aktivnih dostavljaca pokusajte kasnije hvala. ",
            parse_mode="html"
        )
    else:

        question = bot.send_message(
            msg.from_user.id,
            "Dobro dosli nazad. \nSta zelite da porucite danas? \nNapisite sto vise detalja.",
            # f"Welcome back {msg.from_user.first_name}, \n\nWhat would like to order today? \nE.g Flarey sky ",
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
        f"<b>New Order Being Created By @{msg.from_user.id}</b>",
        parse_mode="html",
    )
    order = Order(
        buyer=msg.from_user.username,
        from_id=msg.from_user.id,
        vendor="",
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
        "Molim vas za pick up adresu kao i deo grada.",
        # f"What is the pickup location for this order including the part of the city ? ",
        parse_mode="html"
    )
    bot.register_next_step_handler(question, add_pickup)


def add_pickup(msg):
    "Add pickup spot"
    address = msg.text

    order = db_client.get_order(id=msg.from_user.username)

    if order is None:

        bot.send_message(
            msg.from_user.id,
            "Your do not have an open order. Please start a new order by clicking /order"
        )

    else:
        newOrder = Order(
            buyer=msg.from_user.username,
            from_id=msg.from_user.id,
            vendor="",
            msg_id=order['msg_id'],
            item=order['item'],
            address=address,
            status="created",
            created_at=order['created_at']
        )

        # Update order
        res = db_client.create_update_order(order=newOrder)
        user = db_client.get_user(msg.from_user.id)

        bot.edit_message_text(
            chat_id=CHAT_ID,
            message_id=order['msg_id'],
            text=f"<b>Order Created By @{newOrder.buyer}</b> \nItem: <b>{newOrder.item}</b> \nPickup at: <b>{newOrder.address}</b> \nHome Address: <b>{user['address']}</b>",
            parse_mode="html",
            reply_markup=order_menu()
        )

        bot.send_message(
            msg.from_user.id,
            f"Porudzbina je kreirana, dostavljac ce vam se uskoro javiti. \n\nVasa adresa: {user['address']}",
            # f"You just created a new order, please wait for a courier to pick it up..... \n\nYour Home Address: {user['address']}",
            reply_markup=cancel_menu()
        )


def close_order(msg):
    "This Closes The Order "

    status = db_client.end_order(msg.message.id, "completed")
    print(status)

    order = db_client.get_order_by_msg_id(msg.message.id)

    bot.edit_message_text(
        chat_id=CHAT_ID,
        message_id=order['msg_id'],
        text=f"<b>Order Completed By @{order['vendor']}</b> To <b>@{order['buyer']}</b> \nItem: <b>{order['item']}</b> \nOrder Status: <b>{order['status']}</b>",
        parse_mode="html",
        reply_markup=None
    )

    bot.send_message(
        order['from_id'],
        f"🏭 Order completed by @{order['vendor']}"
    )


def reject_order(msg):
    "Resing Vendor From An Order"
    order = db_client.get_order_by_msg_id(msg.message.id)

    newOrder = Order(
        buyer=order['buyer'],
        from_id=order['from_id'],
        vendor="",
        msg_id=order['msg_id'],
        item=order['item'],
        address=order['address'],
        status="created",
        created_at=order['created_at']
    )

    # Update order
    res = db_client.create_update_order(order=newOrder)
    user = db_client.get_user(newOrder.from_id)

    bot.edit_message_text(
        chat_id=CHAT_ID,
        message_id=order['msg_id'],
        text=f"<b>Order Created By @{newOrder.buyer}</b> \nItem: <b>{newOrder.item}</b> \nPickup at: <b>{newOrder.address}</b> \nHome Address: <b>{user['address']}</b>",
        parse_mode="html",
        reply_markup=order_menu()
    )

    bot.send_message(
        order['from_id'],
        f"🏭 Preuzeta porudzbina je odbijena i vracena na cekanje sacekajte sledeceg kurira @{msg.from_user.username}"
    )


def cancel_order(msg_id):
    "This Closes The Order "

    status = db_client.end_order(msg_id, "canceled")
    print(status)

    order = db_client.get_order_by_msg_id(msg_id)

    bot.edit_message_text(
        chat_id=CHAT_ID,
        message_id=order['msg_id'],
        text=f"Order Canceled  \nItem: <b>{order['item']}</b>",
        parse_mode="html",
        reply_markup=None
    )
    # user = bot.get_chat(order['buyer'])
    # print(user)

    bot.send_message(
        order['from_id'],
        f"🏭 Order has been canceled"
    )
