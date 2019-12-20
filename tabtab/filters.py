import re
from telegram.ext import BaseFilter


class FilterGetMeme(BaseFilter):
    def filter(self, message):
        return message.text == 'Get meme'


class FilterParseMemeName(BaseFilter):
    def filter(self, message):
        pattern = r'[a-z]{4}\d{4}[a-z]{4}$'
        flags = re.IGNORECASE
        if message.text:
            return re.match(pattern, message.text, flags) is not None
        return False


class FilterGetInfo(BaseFilter):
    def filter(self, message):
        return message.text == 'Get info'
