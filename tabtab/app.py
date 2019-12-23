from telethon.sync import TelegramClient, events
from telethon import functions

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
    bot = TelegramClient(
        'bot', config.API_ID, config.API_HASH).start(bot_token=config.BOT_TOKEN)

    @bot.on(events.NewMessage)
    async def any_message_arrived_handler(event):
        chat = await event.get_chat()
        result = await bot(functions.messages.GetFullChatRequest(
            chat_id=chat.id
        ))
        print(result.full_chat.about)

    bot.run_until_disconnected()
