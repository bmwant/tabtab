import logging

from telethon.sync import TelegramClient, events

import config


logging.basicConfig(
   format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
   level=logging.WARNING)


api_id = 107649
api_hash = '4c0cbb403eb99d14e4ba38a4e40c2e13'
bot_token = config.BOT_TOKEN


async def test_client():
   with TelegramClient('name', api_id, api_hash) as client:
      client.send_message('me', 'Hello, myself!')
      print(client.download_profile_photo('me'))

      @client.on(events.NewMessage(pattern='(?i).*Hello'))
      async def handler(event):
         await event.reply('Hey!')

      client.run_until_disconnected()


async def main(bot):

   # Getting information about yourself
   me = await bot.get_me()

   # "me" is an User object. You can pretty-print
   # any Telegram object with the "stringify" method:
   print(me.stringify())


if __name__ == '__main__':
   bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

   @bot.on(events.NewMessage)
   async def my_event_handler(event):
      chat = await event.get_chat()
      from telethon.tl.functions.channels import GetFullChannelRequest
      from telethon import functions, types
      # creating client here
      # ch = client.get_entity("@mychannel")
      entity = await bot.get_entity(chat.id)
      # ch_full = await bot(GetFullChannelRequest(channel=chat))
      result = await bot(functions.messages.GetFullChatRequest(
         chat_id=chat.id
      ))
      print(result.stringify())
      import pdb; pdb.set_trace()
      await event.reply(event.raw_text)

   # with bot:
   #    bot.loop.run_until_complete(main(bot))

   bot.run_until_disconnected()
