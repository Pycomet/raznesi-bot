from config import *
from utils import *
from models import Order


def admin_menu():
    "Attached To Order When In Progress"
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    a = types.InlineKeyboardButton("✔️ Complete", callback_data="done")
    b = types.InlineKeyboardButton("❌ Resign", callback_data="reject")
    keyboard.add(a, b)
    return keyboard


def start_vendor(msg):
    "Add Vendor To An Open Order"
    msg_id = msg.message.id

    order = db_client.get_order_by_msg_id(msg_id)

    if order is None:

        bot.reply_to(
            msg,
            "Order does not exist, please check for new order on the channel"
        )

    else:

        # Check if vendor already exists
        if order['vendor'] not in ["", None]:
            bot.reply_to(
                msg,
                "Sorry, already taken!"
            )
            return

        # Add vendor to order
        updOrder = Order(
            buyer=order['buyer'],
            from_id=order['from_id'],
            vendor=msg.from_user.username,
            msg_id=order['msg_id'],
            item=order['item'],
            address=order['address'],
            active=False,
            status="In progress",
            created_at=order['created_at']
        )
        # Update order
        res = db_client.create_update_order(order=updOrder)
        # user = bot.get_chat(updOrder.buyer)
        buyer = db_client.get_user(updOrder.from_id)

        # Send full details of order
        bot.edit_message_text(
            chat_id=CHAT_ID,
            message_id=order['msg_id'],
            text=f"<b>New Order  By @{updOrder.buyer}</b> \nItem: <b>{updOrder.item}</b> \nPickup at: <b>{updOrder.address}</b> \nHome Address: <b>{buyer.address}</b> \nOrder Status: <b>{updOrder.status}</b> \nCourier: <b>@{updOrder.vendor}</b>",
            parse_mode="html",
            reply_markup=admin_menu()
        )

        bot.send_message(
            updOrder.from_id,
            f"🏭 Order accepted by @{updOrder.vendor}"
        )
