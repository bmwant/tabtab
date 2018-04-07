import sqlite3
from functools import wraps
from contextlib import contextmanager

import  attr

import config


@attr.s
class Meme(object):
    id = attr.ib()
    active = attr.ib()
    alias = attr.ib()
    file_id = attr.ib()
    url = attr.ib()


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
        return func(*args, **kwargs)
    return inner


@with_connection
def insert_new_meme():
    with cursor() as c:
        query = (
            'INSERT INTO meme(active, alias, file_id, url) '
            'VALUES(?, ?, ?, ?);'
        )
        values = (1, 'doge', 'AgADAgADBakxG8zCKEquNQl09cAjNe60qw4ABPRRFzZpUEqWgFkAAgI', 'https://example.com')
        c.execute(query, values)


def get_meme_file_id():
    pass


if __name__ == '__main__':
    insert_new_meme()
