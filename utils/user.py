import io

import PIL.Image

import utils.config

import typing
import telethon.tl.types


default_user_config = {
    'name': '',
    'pronoun_set': 0,
    'anon': [],
}


class User(typing.NamedTuple):
    sender: telethon.tl.types.User | telethon.tl.types.Channel | telethon.tl.types.Chat
    chat_id: int
    client: telethon.client.TelegramClient

    def is_admin(self) -> bool:  # check if in admins list
        return self.sender.id in utils.config.load("config.toml")["admins"]

    async def get_display_name(self) -> str:
        display_name = self.get_param('name')
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
        return f"[{name}](tg://user?id={self.sender.id})"

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

    def get_param(self, param, check_anon: bool = True):
        return self.load_user_config(check_anon)[param]

    def set_param(self, param, val, check_anon: bool = True):
        self.save_user_config(self.load_user_config(check_anon) | {param: val}, check_anon)

    def reset_param(self, param, check_anon: bool = True):
        self.set_param(param, default_user_config[param], check_anon)

    def get_pronouns(self) -> int:
        return self.get_param('pronoun_set')

    def set_pronouns(self, pronoun_set: int):
        if not 0 <= pronoun_set <= 2:
            raise ValueError("Wrong pronoun set number passed")
        self.set_param('pronoun_set', pronoun_set)

    def reset_pronouns(self):
        self.reset_param('pronoun_set')

    def get_name(self) -> str:
        return self.get_param('name')

    def set_name(self, name: str):
        self.set_param('name', name)

    def reset_name(self):
        self.reset_param('name')

    def get_anon_chats(self) -> typing.Set[int]:
        return self.get_param('anon', False)

    def add_anon_chat(self, id: int):
        self.set_param('anon', list(set(self.get_anon_chats()) | {id}))

    def del_anon_chat(self, id: int):
        self.set_param('anon', list(set(self.get_anon_chats()) - {id}))

    def reset_anon_chats(self):
        self.reset_param('anon')

    def is_anon(self, id: int) -> bool:
        return id in self.get_anon_chats()

    def is_self_anon(self, check_anon: bool = True):
        return check_anon and self.is_anon(self.chat_id)


async def from_telethon(user: telethon.tl.types.User | telethon.tl.types.Channel | str | None,
                        chat: telethon.tl.types.Chat | int | None,
                        client: telethon.client.TelegramClient) -> User:
    if type(user) == str:
        return await from_telethon(await client.get_entity(await client.get_input_entity(user)), chat, client)
    if user is not None:
        return User(user, (chat.id if type(chat) != int else chat) if chat else 0, client)
    return User(chat, (chat.id if type(chat) != int else chat) if chat else 0, client)
