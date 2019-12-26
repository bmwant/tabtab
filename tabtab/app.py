from telethon.sync import TelegramClient, events
from telethon import functions

import config
from tabtab.database import insert_new_topic, get_last_topic, Topic
from tabtab.database import insert_new_poll, get_poll_by_message_id, Poll
from tabtab.utils import logger


def check_description_changed(desc: str):
    topic = get_last_topic()
    return topic.text != desc

# '5199659688265777155'


async def handle_polls(bot, event):
    message_id = 27
    chat = await event.get_chat()
    import pdb; pdb.set_trace()
    entity = await bot.get_entity(message_id)
    print(entity)


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

    @bot.on(events.NewMessage)
    async def poll_created_handler(event):
        poll = event.message.poll
        message_id = event.message.id
        await handle_polls(bot, event)
        if event.message.poll is not None:
            results = poll.results
            new_poll = Poll(message_id=message_id)
            insert_new_poll(new_poll)
            print('Total voters', results.total_voters)
            raise events.StopPropagation

    bot.run_until_disconnected()
