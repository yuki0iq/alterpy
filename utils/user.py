import alterpy.context
import dataclasses
import datetime
import io
import PIL.Image
import re
import sqlite3
import telethon.tl.types
import telethon.utils
import utils.common
import utils.log
import utils.str
import utils.regex


con = sqlite3.connect("users.db", autocommit=True)
cur = con.cursor()
cur.execute("PRAGMA journal_mode=WAL")
cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER, name TEXT, pronoun_set TEXT, lang TEXT, replace_id INTEGER, stamp INTEGER)")
cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS users_id ON users(id)")


@dataclasses.dataclass
class User:
    sender: telethon.tl.types.User | telethon.tl.types.Channel | telethon.tl.types.Chat
    chat_id: int
    client: telethon.client.telegramclient.TelegramClient

    def __post_init__(self):
        if cur.execute("SELECT COUNT(*) FROM users WHERE id = ?", (self.sender.id,)).fetchone() == (0,):
            cur.execute("INSERT INTO users VALUES (?, NULL, NULL, NULL, NULL, ?)", (self.sender.id, 0))

    def is_admin(self) -> bool:  # check if in admins list
        return self.sender.id in alterpy.context.admins

    async def get_display_name(self) -> str:
        display_name = self.get_name()
        if display_name:
            return display_name
        if isinstance(self.sender, telethon.tl.types.Channel):
            return str(self.sender.title)
        if not isinstance(self.sender, telethon.tl.types.Chat):
            return str(self.sender.first_name)
        return 'null'

    async def get_mention(self) -> str:
        name = await self.get_display_name()
        # if config.replace_id is set then use id (as user!)
        # user -> tg://user?id=123456789
        # public channel, group -> t.me/username
        rid = self.get_redirect()
        uid = rid or self.sender.id
        username = ''
        if type(self.sender) != telethon.tl.types.User and not rid:
            # use username if applicable
            username = self.sender.username
        if username:
            return f"[{utils.str.escape(name)}](t.me/{username})"
        return f"[{utils.str.escape(name)}](tg://user?id={uid})"

    async def userpic(self) -> PIL.Image.Image | None:
        by = io.BytesIO()
        await self.client.download_profile_photo(self.sender, file=by)
        by.seek(0)
        try:
            return PIL.Image.open(by)
        except:
            return None

    def get_pronouns(self) -> list[int]:
        (pronouns,) = cur.execute("SELECT pronoun_set FROM users WHERE id = ?", (self.sender.id,)).fetchone()
        if pronouns is None:
            return None
        assert pronouns.isdigit()
        return list(map(int, pronouns))

    def set_pronouns(self, pronoun_set: None | list[int]):
        cur.execute(
            "UPDATE users SET pronoun_set = ?, stamp = ? WHERE id = ?",
            (
                pronoun_set and ''.join(map(str, pronoun_set)),
                utils.common.stamp(),
                self.sender.id
            )
        )

    def get_name(self) -> str | None:
        return cur.execute("SELECT name FROM users WHERE id = ?", (self.sender.id,)).fetchone()[0]

    def set_name(self, name: None | str):
        cur.execute("UPDATE users SET name = ?, stamp = ? WHERE id = ?", (name, utils.common.stamp(), self.sender.id))

    def get_redirect(self) -> int | None:
        return cur.execute("SELECT replace_id FROM users WHERE id = ?", (self.sender.id,)).fetchone()[0]

    def set_redirect(self, uid: int):
        cur.execute("UPDATE users SET replace_id = ?, stamp = ? WHERE id = ?", (uid, utils.common.stamp(), self.sender.id))

    def get_lang(self) -> str:
        return cur.execute("SELECT lang FROM users WHERE id = ?", (self.sender.id,)).fetchone()[0]

    def set_lang(self, lang: str):
        cur.execute("UPDATE users SET lang = ?, stamp = ? WHERE id = ?", (lang, utils.common.stamp(), self.sender.id))


async def from_telethon(user: telethon.tl.types.User | telethon.tl.types.Channel | telethon.tl.types.Chat | str | int,
                        chat: telethon.tl.types.Chat | int | None,
                        client: telethon.client.telegramclient.TelegramClient) -> User:
    if isinstance(user, (str, int)):
        return await from_telethon(await client.get_entity(await client.get_input_entity(user)), chat, client)
    if not user:
        return await from_telethon(chat, chat, client)
    if isinstance(chat, int):
        chat_id = chat
    else:
        chat_id = chat.id if chat else 0
    return User(user, chat_id, client)


# mention:
#  OR:
#    @(username)
#      where username is (a-zA-Z0-9_){5,64} and can't start with digit
#                        -> using simple check (word-like character)
#    {(uid)|(len)}(name)
#      where uid  is number
#            len  is number
#            name is string of len=len
mention_pattern = utils.regex.ignore_case(
    utils.regex.unite(
        '@' + utils.regex.named('username', r'\w+'),
        r'\{' + utils.regex.named_int('uid') + r'\|' + utils.regex.named_int('len') + r'\}'
    )
)


async def from_str(arg: str, chat_id: int, client: telethon.client.telegramclient.TelegramClient) -> tuple[str, User | None, str, str]:
    match = re.search(utils.user.mention_pattern, arg)
    if not match:
        return arg, None, '', ''

    m = match[0]
    idx = match.span()[0]
    pre_arg, arg = arg[:idx], arg[idx:]

    # if matched 'username' then get name
    # if matched 'uid + len' then get name from text
    vars = match.groupdict()

    if vars['username'] is not None:
        username, arg = m[1:], arg[len(m):]
        try:
            cur_user = await utils.user.from_telethon(username, chat=chat_id, client=client)
            mention = await cur_user.get_mention()
        except ValueError:
            cur_user = None
            mention = f"@{username}"
    else:
        uid = int(vars['uid'])
        l = int(vars['len'])
        arg = arg[len(m):]
        name, arg = arg[:l], arg[l:]
        cur_user = await utils.user.from_telethon(uid, chat=chat_id, client=client)
        mention = f"[{utils.str.escape(name)}](tg://user?id={uid})"

    return pre_arg, cur_user, mention, arg

