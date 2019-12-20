#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)

import config
from tabtab import handlers
from tabtab.utils import logger


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def run():
    logger.info('Bot is running...')
    updater = Updater(token=config.BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text,
                                  handlers.check_description_changed))

    # filter_get_info = FilterGetInfo()
    # filter_get_meme = FilterGetMeme()
    # dp.add_handler(MessageHandler(filter_get_info,
    #                               handlers.get_info_callback))
    # dp.add_handler(MessageHandler(filter_get_meme,
    #                               handlers.get_meme_callback))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
