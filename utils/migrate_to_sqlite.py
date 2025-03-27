import pytomlpp
import sqlite3
import utils.file

con = sqlite3.connect("users.db", autocommit=True)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(id PRIMARY KEY, name, pronoun_set, lang, replace_id)")

for filename in utils.file.list_files("user/"):
    config = pytomlpp.load(f"user/{filename}")

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

    cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (user_id, name, pronoun_set, lang, replace_id,))
