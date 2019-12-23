from telethon.sync import TelegramClient, events
from telethon import functions

import config
from tabtab.database import insert_new_topic, get_last_topic, Topic
from tabtab.utils import logger


def check_description_changed(desc: str):
    topic = get_last_topic()
    return topic.text != desc


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
        description = result.full_chat.about
        if check_description_changed(description):
            new_topic = Topic(text=description)
            insert_new_topic(new_topic)
            logger.debug(
                'Group "%s" had description changed to "%s"',
                chat.title, description
            )
            await bot.send_message(
                chat.id, f'Вова знову поміняв опис!\n**{description}**')

    bot.run_until_disconnected()
