from tabtab.utils import logger, restricted
from tabtab.database import insert_new_topic, get_last_topic, Topic


def meme_name_handler(bot, update):

    # We already have partial meme, so continue with creation
    return memes_uploader_step2(bot, update)


def check_description_changed(update, context):
    chat_id = update.effective_chat.id
    group = context.bot.get_chat(chat_id)
    print(group.description, group.title)
    text = group.description
    topic = get_last_topic()
    if topic.text != text:
        new_topic = Topic(text=text)
        insert_new_topic(new_topic)
        logger.debug(
            'Group "%s" had description changed to "%s"', group.title, text)
        update.message.reply_text(update.message.text, quote=False)


@restricted
def memes_uploader_step2(bot, update):
    bot.tmp_meme.alias = update.message.text.strip().lower()
    logger.debug('Got an alias for a meme')
    update.message.reply_text('Now enter a url for a meme')


@restricted
def memes_uploader_step3(bot, update):
    bot.tmp_meme.url = update.message.text
    logger.debug('Got url for a meme')
    # Reset state
    bot.tmp_meme = None
    update.message.reply_text('New meme added successfully')


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
