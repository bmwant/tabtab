import sqlite3
from functools import wraps
from contextlib import contextmanager

import attr

import config
from tabtab.utils import logger


@attr.s
class Meme(object):
    id = attr.ib(default=None)
    active = attr.ib(default=1)
    alias = attr.ib(default=None)
    file_id = attr.ib(default=None)
    url = attr.ib(default=None)


@attr.s
class Topic(object):
    created = attr.ib(default=None)
    text = attr.ib(default='')


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
def insert_new_meme(cursor, meme):
    query = (
        'INSERT INTO meme(active, alias, file_id, url) '
        'VALUES(?, ?, ?, ?);'
    )
    logger.debug('Inserting %s...' % meme)
    values = (1, meme.alias, meme.file_id, meme.url)
    cursor.execute(query, values)


@with_connection
def get_meme_by_alias(cursor, alias):
    query = (
        'SELECT * FROM meme WHERE alias = ?;'
    )
    cursor.execute(query, (alias,))
    res = cursor.fetchone()
    if res is None:
        raise ValueError('No such meme %s' % alias)
    return Meme(*res)


if __name__ == '__main__':
    t1 = Topic(text='Test topic 1')
    t2 = Topic(text='Test topic 2')
    insert_new_topic(t1)
    insert_new_topic(t2)
