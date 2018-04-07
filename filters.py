from telegram.ext import BaseFilter


class FilterGetMeme(BaseFilter):
    def filter(self, message):
        return message.text == 'Get meme'


class FilterGetInfo(BaseFilter):
    def filter(self, message):
        return message.text == 'Get info'
