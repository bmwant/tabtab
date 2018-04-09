#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (
    LabeledPrice,
    ShippingOption,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    MessageEntity,
    InlineKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
    CallbackQueryHandler,

)
from filters import FilterGetInfo, FilterGetMeme, FilterMemeName


import config
from utils import logger
from database import Meme, insert_new_meme


TMP_MEME = Meme()


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


def start_with_shipping_callback(bot, update):
    chat_id = update.message.chat_id
    title = "Payment Example"
    description = "Payment Example using python-telegram-bot"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    provider_token = config.PAYMENTWALL_TEST_TOKEN
    start_parameter = "test-payment"
    # https://core.telegram.org/bots/payments#supported-currencies
    currency = "UAH"
    price = 100
    prices = [LabeledPrice("Test", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    bot.sendInvoice(chat_id, title, description, payload,
                    provider_token, start_parameter, currency, prices,
                    need_name=True, need_phone_number=True,
                    need_email=True, need_shipping_address=True, is_flexible=True)


def start_without_shipping_callback(bot, update):
    chat_id = update.message.chat_id
    title = "Payment Example"
    description = "Payment Example using python-telegram-bot"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    provider_token = "PROVIDER_TOKEN"
    start_parameter = "test-payment"
    currency = "USD"
    # price in dollars
    price = 1
    # price * 100 so as to include 2 d.p.
    prices = [LabeledPrice("Test", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    bot.sendInvoice(chat_id, title, description, payload,
                    provider_token, start_parameter, currency, prices)


def shipping_callback(bot, update):
    query = update.shipping_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Custom-Payload':
        # answer False pre_checkout_query
        bot.answer_shipping_query(shipping_query_id=query.id, ok=False,
                                  error_message="Something went wrong...")
        return
    else:
        options = list()
        # a single LabeledPrice
        options.append(ShippingOption('1', 'Shipping Option A', [LabeledPrice('A', 100)]))
        # an array of LabeledPrice objects
        price_list = [LabeledPrice('B1', 150), LabeledPrice('B2', 200)]
        options.append(ShippingOption('2', 'Shipping Option B', price_list))
        bot.answer_shipping_query(shipping_query_id=query.id, ok=True,
                                  shipping_options=options)


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


def the_callback(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def memes_uploader_step1(bot, update):
    global TMP_MEME
    photo = update.message.photo[-1]
    file = photo.get_file()
    TMP_MEME.file_id = file.file_id
    logger.debug('Get image for a meme')
    update.message.reply_text('Now enter alias for the meme')


def memes_uploader_step2(bot, update):
    global TMP_MEME
    TMP_MEME.alias = update.message.text
    logger.debug('Got an alias for a meme')
    update.message.reply_text('Now enter a url for a meme')


def memes_uploader_step3(bot, update):
    global TMP_MEME
    TMP_MEME.url = update.message.text
    logger.debug('Got url for a meme')
    _insert_new_meme(TMP_MEME)
    TMP_MEME = Meme()  # Reset global state
    update.message.reply_text('New meme added successfully')


def _insert_new_meme(tmp_meme):
    insert_new_meme(tmp_meme)
    logger.info('Successfully registered new meme %s' % tmp_meme.alias)


def send_meme_back(bot, update):
    file_id = 'AgADAgADBakxG8zCKEquNQl09cAjNe60qw4ABPRRFzZpUEqWgFkAAgI'
    bot.send_photo(chat_id=update.effective_chat.id, photo=file_id)


def get_meme_callback(bot, update):
    chat_id = update.message.chat_id
    message = (
        'Enter a meme name to get a picture for it'
    )
    bot.send_message(
        chat_id,
        message,
    )


def get_info_callback(bot, update):
    chat_id = update.message.chat_id
    message = (
        'Some information about this bot\n'
        'And how to get a meme by a name\n'
    )
    bot.send_message(
        chat_id,
        message,
    )


def main():
    logger.info('Bot is running...')
    updater = Updater(token=config.BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_callback))
    dp.add_handler(CommandHandler('give', send_meme_back))

    # Add command handler to start the payment invoice
    dp.add_handler(CommandHandler("shipping", start_with_shipping_callback))

    # Optional handler if your product requires shipping
    dp.add_handler(ShippingQueryHandler(shipping_callback))

    dp.add_handler(MessageHandler(Filters.photo, memes_uploader_step1))
    filter_meme_name = FilterMemeName()
    dp.add_handler(MessageHandler(filter_meme_name, memes_uploader_step2))
    dp.add_handler(MessageHandler(
        Filters.entity(MessageEntity.URL) |
        Filters.entity(MessageEntity.TEXT_LINK),
        memes_uploader_step3))
    # Pre-checkout handler to final check
    dp.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Success! Notify your user!
    dp.add_handler(MessageHandler(Filters.successful_payment,
                                  successful_payment_callback))
    dp.add_handler(CallbackQueryHandler(the_callback))

    filter_get_meme = FilterGetMeme()
    filter_get_info = FilterGetInfo()
    dp.add_handler(MessageHandler(filter_get_meme, get_meme_callback))
    dp.add_handler(MessageHandler(filter_get_info, get_info_callback))

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
