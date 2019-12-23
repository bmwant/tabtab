## tabtab

Funny telegram bot.

Current features:

* Posting a message in a group when its description changes

### Development

Create a database

```
$ sqlite3 database.db < init_database.sql
```

Test inserts

```bash
$ sqlite3 database.db
sqlite>.databases
sqlite>INSERT INTO topic(text) VALUES ('test topic');
sqlite>SELECT * FROM topic;
```

Run database-related operations

```bash
$ poetry run python database.py
2019-12-19 12:57:42,421 - utils - DEBUG - Inserting Topic(created=None, text='Test topic 1')...
2019-12-19 12:57:42,422 - utils - DEBUG - Inserting Topic(created=None, text='Test topic 2')...
```


### Deployment


```bash
$ cd deployment
$ poetry run ansible-playbook -vv init.yml --vault-password-file ~/.vault
```
