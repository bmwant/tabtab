import sqlite3
from functools import wraps
from contextlib import contextmanager

import attr

import config
from tabtab.utils import logger


@attr.s
class Topic(object):
    created = attr.ib(default=None)
    text = attr.ib(default='')


@attr.s
class Poll(object):
    message_id = attr.ib(default=None)
    casted = attr.ib(default=0)


@contextmanager
def cursor():
    conn = sqlite3.connect(config.DATABASE)
    c = conn.cursor()

    yield c

    conn.commit()
    conn.close()


def with_connection(func):
    @wraps(func)
    def inner(*args, **kwargs):
        with cursor() as c:
            return func(c, *args, **kwargs)
    return inner


@with_connection
def insert_new_topic(cursor, topic):
    query = (
        'INSERT INTO topic(text) '
        'VALUES(?);'
    )
    logger.debug('Inserting %s...' % topic)
    values = (topic.text, )
    cursor.execute(query, values)


@with_connection
def get_last_topic(cursor):
    query = (
        'SELECT * FROM topic '
        'ORDER BY datetime(created) DESC, rowid DESC LIMIT 1;'
    )
    logger.debug('Fetching current topic...')
    cursor.execute(query)
    res = cursor.fetchone() or {}
    return Topic(*res)


@with_connection
def insert_new_poll(cursor, poll):
    query = (
        'INSERT INTO poll(message_id, casted) '
        'VALUES(?, ?);'
    )
    logger.debug('Inserting %s...' % poll)
    values = (poll.message_id, poll.casted)
    cursor.execute(query, values)


@with_connection
def get_poll_by_message_id(cursor, message_id: int):
    query = (
        'SELECT * FROM poll WHERE id = ?;'
    )
    cursor.execute(query, (message_id,))
    res = cursor.fetchone()
    if res is None:
        raise ValueError('No such record %s' % message_id)
    return Poll(*res)
