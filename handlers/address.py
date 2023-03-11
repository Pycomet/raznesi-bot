from config import *
from utils import *
from .start import start_new_user
from models import User


@bot.message_handler(commands=['address'])
def start_addr(msg):
    "Change Address"
    user = db_client.get_user(msg.from_user.id)

    if user is None:
        bot.send_message(
            msg.from_user.id,
            "Please click /start to begin using this service. You do not have an account."
        )
    else:
        question = bot.send_message(
            msg.from_user.id,
            "Pošaljite vašu kućnu adresu uključujući i deo grada."
            # "To update your account, please provide your new valid home address including the part of the city"
        )
        bot.register_next_step_handler(question, start_new_user)
