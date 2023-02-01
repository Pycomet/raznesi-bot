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
            "To have your account registered, please provide your valid home address"
        )
        bot.register_next_step_handler(question, start_new_user)
