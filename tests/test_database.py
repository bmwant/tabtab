from tabtab.database import Topic
from tabtab.database import insert_new_topic, get_last_topic


def test_insert_new_topic():
    t1 = Topic(text='Test topic 1')
    t2 = Topic(text='Test topic 2')
    insert_new_topic(t1)
    insert_new_topic(t2)


def test_get_last_topic():
    topic = get_last_topic()
    print(topic)
