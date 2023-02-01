from config import *
from utils import *


@bot.message_handler(commands=["mute"])
def mutebot(msg):
    "Mute The Bot From Responding"

    if hasattr(msg, "message_id") and msg.chat.type != 'group':
        bot.delete_message(msg.chat.id, msg.message_id)

    if msg.from_user.username == ADMIN:
        handler_state["Requests"] = True
        bot.send_message(
            msg.chat.id,
            f" 🔇 Silent Mode Activated. \n\nThis Bot Would Not Take Any Incoming Orders",
            parse_mode="html",
        )


@bot.message_handler(commands=["unmute"])
def mutebot(msg):
    "Mute The Bot From Responding"

    if hasattr(msg, "message_id") and msg.chat.type != 'group':
        bot.delete_message(msg.chat.id, msg.message_id)

    if msg.from_user.username == ADMIN:
        handler_state["Requests"] = False
        bot.send_message(
            msg.chat.id,
            f" 🔊 Silent Mode Deactivated. \n\nBot is Actively Taking Orders",
            parse_mode="html",
        )
