import logging
from functools import wraps

import config


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user = update.effective_user
        if user.id not in config.LIST_OF_ADMINS:
            logger.critical('Unauthorized access denied for %s.' % user.id)
            logger.debug('User info %s', user)
            return
        return func(bot, update, *args, **kwargs)
    return wrapped
