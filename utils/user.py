import context
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
    'lang': 'en',
    'replace_id': 0
}


class User(typing.NamedTuple):
    sender: typing.Union[telethon.tl.types.User, telethon.tl.types.Channel, telethon.tl.types.Chat]
    chat_id: int
    client: telethon.client.telegramclient.TelegramClient

    def is_admin(self) -> bool:  # check if in admins list
        return self.sender.id in context.admins

    async def get_display_name(self) -> str:
        display_name = self.get('name')
        if display_name:
            return display_name
        if type(self.sender) == telethon.tl.types.Channel:
            return self.sender.title
        if type(self.sender) != telethon.tl.types.Chat:
            return self.sender.first_name
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

    async def userpic(self) -> typing.Optional[PIL.Image.Image]:
        by = io.BytesIO()
        await self.client.download_profile_photo(self.sender, file=by)
        by.seek(0)
        try:
            return PIL.Image.open(by)
        except:
            return None

    def config_name(self) -> str: return f"user/{self.sender.id}.toml"

    def load_user_config(self) -> dict[str, typing.Any]: return default_user_config | utils.config.load(self.config_name())
    def save_user_config(self, conf: dict[str, typing.Any]): utils.config.save(self.config_name(), conf)

    def get(self, param: str) -> typing.Any: return self.load_user_config()[param]
    def set(self, param: str, val: typing.Any) -> None: self.save_user_config(self.load_user_config() | {param: val})
    def reset(self, param: str) -> None: self.set(param, default_user_config[param])

    def get_pronouns(self) -> typing.Union[int, list[int]]: return self.get('pronoun_set')
    def set_pronouns(self, pronoun_set: typing.Union[int, list[int]]) -> None: self.set('pronoun_set', pronoun_set)
    def reset_pronouns(self) -> None: self.reset('pronoun_set')

    def get_name(self) -> str: return self.get('name')
    def set_name(self, name: str) -> None: self.set('name', name)
    def reset_name(self) -> None: self.reset('name')

    def get_redirect(self) -> str: return self.get('replace_id')
    def set_redirect(self, uid: int) -> None: self.set('replace_id', uid)
    def reset_redirect(self) -> None: self.reset('replace_id')

    def get_lang(self) -> str: return self.get('lang')
    def set_lang(self, lang: str) -> None: self.set('lang', lang)
    def reset_lang(self) -> None: self.reset('lang')


async def from_telethon(user: typing.Union[telethon.tl.types.User, telethon.tl.types.Channel, telethon.tl.types.Chat, str, int],
                        chat: typing.Union[telethon.tl.types.Chat, int, None],
                        client: telethon.client.telegramclient.TelegramClient) -> User:
    if type(user) == str or type(user) == int:
        return await from_telethon(await client.get_entity(await client.get_input_entity(user)), chat, client)
    if user is not None:
        if type(chat) == int:
            chat_id = chat
        else:
            chat_id = chat.id if chat else 0
        return User(user, chat_id, client)
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


async def from_str(arg: str, chat_id: int, client: telethon.client.telegramclient.TelegramClient) -> tuple[str, typing.Optional[User], str, str]:
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

