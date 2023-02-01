from config import *
from utils import *


# def start_menu():
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     a = types.InlineKeyboardButton("Create New Order", callback_data="order")
#     keyboard.add(a)
#     return keyboard


@bot.message_handler(commands=['start'])
def startbot(msg):
    # import pdb; pdb.set_trace(
    bot.send_chat_action(msg.from_user.id, "typing")

    "Ignites the bot application to take action"
    user = db_client.get_user(msg.from_user.id)

    if user is None:

        question = bot.send_message(
            msg.from_user.id,
            "To have your account registered, please provide your valid home address including the part of the city"
        )
        bot.register_next_step_handler(question, start_new_user)

    else:
        bot.send_message(
            msg.from_user.id,
            "Welcome to the <b>Offical Reznesi's Order Bot </b> \n\nClick /order to place an order",
            parse_mode="html"
        )


@bot.message_handler(regexp="^Back")
def startbotn(msg):
    startbot(msg)


def start_new_user(msg):

    if msg.from_user.username is None:
        bot.send_message(
            msg.from_user.id,
            "Please attach a username to your account! Check your settings to be sure to have one, I can not register you on our database without one"
        )
    else:

        address = msg.text
        bot.send_chat_action(msg.from_user.id, "typing")

        user = User(user_id=msg.from_user.id, address=address)
        # Create user
        res = db_client.create_update_user(user=user)
        print(res)

        bot.send_message(
            msg.from_user.id,
            "Account Created. Create your first order by clicking"
        )
