import os
import datetime

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from SaitamaRobot import dispatcher
from SaitamaRobot.modules.helper_funcs.chat_status import dev_plus


@dev_plus
def logs(update: Update, context: CallbackContext):
    user = update.effective_user
    with open("log.txt", "rb") as f:
        context.bot.send_document(document=f, filename=f.name, chat_id=user.id)


LOG_HANDLER = CommandHandler("logs", logs, run_async=True)

dispatcher.add_handler(LOG_HANDLER)

__mod_name__ = "Debug"
