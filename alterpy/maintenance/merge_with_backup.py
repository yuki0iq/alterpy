import os
import sqlite3

con = sqlite3.connect(os.environ["DATABASE"], autocommit=True)
cur = con.cursor()

reference_con = sqlite3.connect(os.environ["REFERENCE"])
reference_cur = reference_con.cursor()

for (user_id, name, pronoun_set, lang, replace_id, stamp) in reference_cur.execute("SELECT id, name, pronoun_set, lang, replace_id, stamp FROM users"):
    if cur.execute("SELECT COUNT(*) FROM users WHERE id = ?", (user_id,)).fetchone() == (0,):
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (user_id, name, pronoun_set, lang, replace_id, stamp))
    else:
        cur.execute(
            "UPDATE users SET name = ?, pronoun_set = ?, lang = ?, replace_id = ?, stamp = ? WHERE id = ? AND stamp < ?",
            (name, pronoun_set, lang, replace_id, stamp, user_id, stamp)
        )
