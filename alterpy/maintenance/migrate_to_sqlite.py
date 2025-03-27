import os
import pytomlpp
import sqlite3
import utils.file

con = sqlite3.connect(os.environ["MIGRATED"], autocommit=True)
cur = con.cursor()
cur.execute("PRAGMA journal_mode=WAL")
cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER, name TEXT, pronoun_set TEXT, lang TEXT, replace_id INTEGER, stamp INTEGER)")
cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS users_id ON users(id)")

for filename in utils.file.list_files("user/"):
    config = pytomlpp.load(f"user/{filename}")

    stamp = os.stat(f"user/{filename}").st_mtime_ns // 1000

    user_id = int(filename[:-5])

    name = config.get('name')
    if name == '':
        name = None

    pronoun_set = config.get('pronoun_set')
    if isinstance(pronoun_set, int):
        pronoun_set = [pronoun_set]
    if pronoun_set:
        pronoun_set = ''.join(map(str, pronoun_set))
    if pronoun_set == '0':
        pronoun_set = None

    lang = config.get('lang')
    if lang == 'en':
        lang = None

    replace_id = config.get('replace_id')
    if replace_id == 0:
        replace_id = None

    # print(user_id, repr(name), repr(pronoun_set), repr(lang), repr(replace_id))
    cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (user_id, name, pronoun_set, lang, replace_id, stamp))
