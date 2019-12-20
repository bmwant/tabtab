from tabtab.utils import logger, restricted
from tabtab.database import insert_new_meme, get_meme_by_alias


def meme_name_handler(bot, update):
    if getattr(bot, 'tmp_meme', None) is None:
        return send_meme_back(bot, update)

    # We already have partial meme, so continue with creation
    return memes_uploader_step2(bot, update)


def echo(update, context):
    logger.debug('Yes, we should be here')
    update.message.reply_text(update.message.text)


@restricted
def memes_uploader_step2(bot, update):
    bot.tmp_meme.alias = update.message.text.strip().lower()
    logger.debug('Got an alias for a meme')
    update.message.reply_text('Now enter a url for a meme')


@restricted
def memes_uploader_step3(bot, update):
    bot.tmp_meme.url = update.message.text
    logger.debug('Got url for a meme')
    _insert_new_meme(bot.tmp_meme)
    # Reset state
    bot.tmp_meme = None
    update.message.reply_text('New meme added successfully')


def _insert_new_meme(tmp_meme):
    insert_new_meme(tmp_meme)
    logger.info('Successfully registered new meme %s' % tmp_meme.alias)


def send_meme_back(bot, update):
    alias = update.message.text.strip().lower()

    try:
        meme = get_meme_by_alias(alias)
        bot.send_photo(chat_id=update.effective_chat.id, photo=meme.file_id)
    except ValueError:
        update.message.reply_text('No meme with such name %s!' % alias)


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
