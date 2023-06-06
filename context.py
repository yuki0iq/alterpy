import aiohttp
import typing


the_bot_id = 0
admins: set[int] = set()
session: typing.Optional[aiohttp.ClientSession] = None

