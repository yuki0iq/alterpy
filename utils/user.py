import utils.config
import utils.str
import utils.log
import utils.regex
import re

import typing
import telethon.tl.types
import telethon.utils
import PIL.Image
import io


default_user_config = {
    'name': '',
    'pronoun_set': 0,
    'anon': [],
    'replace_id': 0
}


class User(typing.NamedTuple):
    sender: telethon.tl.types.User | telethon.tl.types.Channel | telethon.tl.types.Chat
    chat_id: int
    client: telethon.client.TelegramClient

    def is_admin(self) -> bool:  # check if in admins list
        return self.sender.id in utils.config.load("config.toml")["admins"]

    async def get_display_name(self) -> str:
        display_name = self.get('name')
        if display_name:
            return display_name
        if type(self.sender) == telethon.tl.types.Channel:
            return self.sender.title
        try:
            return self.sender.first_name
        except:
            return 'null'

    async def get_mention(self) -> str:
        name = await self.get_display_name()
        # if config.replace_id is set then use id (as user!)
        # user -> tg://user?id=123456789
        # public channel, group -> t.me/username
        rid = self.get('replace_id')
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

    def config_name(self) -> str:
        return f"user/{self.sender.id}.toml"

    def load_user_config(self, check_anon: bool = True):
        return default_user_config | (utils.config.load(self.config_name()) if not self.is_self_anon(check_anon) else {})

    def save_user_config(self, conf, check_anon: bool = True):
        if not self.is_self_anon(check_anon):
            utils.config.save(self.config_name(), conf)

    def get(self, param, check_anon: bool = True): return self.load_user_config(check_anon)[param]
    def set(self, param, val, check_anon: bool = True): self.save_user_config(self.load_user_config(check_anon) | {param: val}, check_anon)
    def reset(self, param, check_anon: bool = True): self.set(param, default_user_config[param], check_anon)

    def get_pronouns(self) -> int | list[int]: return self.get('pronoun_set')
    def set_pronouns(self, pronoun_set: int | list[int]): self.set('pronoun_set', pronoun_set)
    def reset_pronouns(self): self.reset('pronoun_set')

    def get_name(self) -> str: return self.get('name')
    def set_name(self, name: str): self.set('name', name)
    def reset_name(self): self.reset('name')

    def get_redirect(self) -> str: return self.get('replace_id')
    def set_redirect(self, uid: int): self.set('replace_id', uid)
    def reset_redirect(self): self.reset('replace_id')

    def get_anon_chats(self) -> typing.Set[int]: return self.get('anon', False)
    def add_anon_chat(self, id: int): self.set('anon', list(set(self.get_anon_chats()) | {id}))
    def del_anon_chat(self, id: int): self.set('anon', list(set(self.get_anon_chats()) - {id}))
    def reset_anon_chats(self): self.reset('anon')

    def is_anon(self, id: int) -> bool: return id in self.get_anon_chats()
    def is_self_anon(self, check_anon: bool = True): return check_anon and self.is_anon(self.chat_id)


async def from_telethon(user: telethon.tl.types.User | telethon.tl.types.Channel | str | int | None,
                        chat: telethon.tl.types.Chat | int | None,
                        client: telethon.client.TelegramClient) -> User:
    if type(user) == str or type(user) == int:
        return await from_telethon(await client.get_entity(await client.get_input_entity(user)), chat, client)
    if user is not None:
        return User(user, (chat.id if type(chat) != int else chat) if chat else 0, client)
    return await from_telethon(chat, chat, client)


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


async def from_str(arg: str, chat_id: int, client: telethon.client.TelegramClient) -> tuple[str, User|None, str, str]:
    match = re.search(utils.user.mention_pattern, arg)
    if not match:
        return arg, None, '', ''

    m = match[0]
    pre_arg = arg[:match.endpos - len(m)]

    # if matched 'username' then get name
    # if matched 'uid + len' then get name from text
    vars = match.groupdict()

    if vars['username'] is not None:
        username, arg = m[1:], arg[len(m):]
        cur_user = await utils.user.from_telethon(username, chat=chat_id, client=client)
        mention = await cur_user.get_mention()
    else:
        uid = int(vars['uid'])
        l = int(vars['len'])
        arg = arg[len(m):]
        name, arg = arg[:l], arg[l:]
        cur_user = await utils.user.from_telethon(uid, chat=chat_id, client=client)
        mention = f"[{utils.str.escape(name)}](tg://user?id={uid})"

    return pre_arg, cur_user, mention, arg

