#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (
    LabeledPrice,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    MessageEntity,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
)


import config
import handlers
from utils import logger
from filters import FilterGetInfo, FilterParseMemeName, FilterGetMeme


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def start_callback(bot, update):
    button_list = [
        InlineKeyboardButton('Get meme'),
        InlineKeyboardButton('Get info'),
    ]
    chat_id = update.message.chat_id
    reply_markup = ReplyKeyboardMarkup([button_list], one_time_keyboard=True)
    bot.send_message(
        chat_id,
        'Press get meme and enter meme name',
        reply_markup=reply_markup,
    )


def start_without_shipping_callback(bot, update):
    chat_id = update.message.chat_id
    title = "Payment Example"
    description = "Payment Example using python-telegram-bot"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    # See https://core.telegram.org/bots/payments#getting-a-token
    provider_token = config.PAYMENTWALL_TEST_TOKEN
    start_parameter = "test-payment"
    # https://core.telegram.org/bots/payments#supported-currencies
    currency = 'UAH'
    price = 100
    # price * 100 so as to include 2 d.p.
    prices = [LabeledPrice("Test", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    bot.sendInvoice(chat_id, title, description, payload,
                    provider_token, start_parameter, currency, prices)


# after (optional) shipping, it's the pre-checkout
def precheckout_callback(bot, update):
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Custom-Payload':
        # answer False pre_checkout_query
        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=False,
                                      error_message="Something went wrong...")
    else:
        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)


# finally, after contacting to the payment provider...
def successful_payment_callback(bot, update):
    # do something after successful receive of payment?
    update.message.reply_text("Thank you for your payment!")


def main():
    logger.info('Bot is running...')
    updater = Updater(token=config.BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_callback))

    # Add command handler to start the payment invoice
    dp.add_handler(CommandHandler('pay', start_without_shipping_callback))

    dp.add_handler(MessageHandler(Filters.photo,
                                  handlers.memes_uploader_step1))
    filter_meme_name = FilterParseMemeName()
    dp.add_handler(MessageHandler(filter_meme_name,
                                  handlers.meme_name_handler))
    dp.add_handler(MessageHandler(
        Filters.entity(MessageEntity.URL) |
        Filters.entity(MessageEntity.TEXT_LINK),
        handlers.memes_uploader_step3))
    # Pre-checkout handler to final check
    dp.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Success! Notify your user!
    dp.add_handler(MessageHandler(Filters.successful_payment,
                                  successful_payment_callback))

    filter_get_info = FilterGetInfo()
    filter_get_meme = FilterGetMeme()
    dp.add_handler(MessageHandler(filter_get_info,
                                  handlers.get_info_callback))
    dp.add_handler(MessageHandler(filter_get_meme,
                                  handlers.get_meme_callback))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
