from telegram.ext import (
    CommandHandler, CallbackContext,
    ConversationHandler, MessageHandler,
    Filters, Updater, CallbackQueryHandler
)
import os
import handlers

updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True)

dispatcher = updater.dispatcher


def main():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start)],
        states={
            handlers.ADD_USER: [MessageHandler(Filters.all, handlers.add_new_user)],
            handlers.BUSINESS_INFO: [MessageHandler(Filters.all, handlers.update_biz_info)]
        },
        allow_reentry=True,
        fallbacks=[CommandHandler('cancel', handlers.cancel)]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()
