# Adapted from <https://github.com/monosans/aiobalaboba>

import sys
from typing import List, Optional, Union, NamedTuple, Any, Literal
from aiohttp import ClientResponse, ClientSession
import utils.str


class TextType(NamedTuple):
    number: int
    name: str
    description: str

def get_headers(input: str, style_id: int = 0, lang: str = 'ru'):
    user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0"
    origin = "https://yandex.ru" if lang == 'ru' else "https://yandex.com"
    referer = f"https://yandex.ru/lab/yalm?style={style_id}" if lang == 'ru' else f"https://yandex.com/lab/yalm-en?style={style_id}"
    x_requested_with = "XMLHttpRequest"
    x_retpath_y = f"{referer}&input={utils.str.urlencode(input)}&skipCurtain=1"
    return {'User-Agent': user_agent, 'Origin': origin, 'Referer': referer, 'X-Requested-With': x_requested_with, 'X-Retpath-Y': x_retpath_y}


class HTTPSession:
    __slots__ = ("session",)

    def __init__(self, session: Optional[ClientSession]) -> None:
        self.session = session

    async def get_response(
        self, *, method: str, endpoint: str, json: Any = None, headers: Optional[dict] = None
    ) -> Any:
        if isinstance(self.session, ClientSession) and not self.session.closed:
            response = await self._fetch(
                method=method, endpoint=endpoint, json=json, session=self.session, headers=headers
            )
        else:
            async with ClientSession() as session:
                response = await self._fetch(
                    method=method, endpoint=endpoint, json=json, session=session, headers=headers
                )
        return await response.json()

    async def _fetch(
        self, *, method: str, endpoint: str, json: Any, session: ClientSession, headers: Optional[dict]
    ) -> ClientResponse:
        async with session.request(
            method,
            f"https://yandex.ru/lab/api/yalm/{endpoint}",
            json=json,
            raise_for_status=True,
            headers=headers
        ) as response:
            await response.read()
        return response


class Balaboba:
    """Asynchronous wrapper for Yandex Balaboba."""

    __slots__ = ("_session",)

    def __init__(self, session: Optional[ClientSession] = None) -> None:
        """Asynchronous wrapper for Yandex Balaboba."""
        self._session = HTTPSession(session)

    @property
    def session(self) -> Optional[ClientSession]:
        return self._session.session

    @session.setter
    def session(self, session: Optional[ClientSession]) -> None:
        self._session.session = session

    async def get_text_types(
        self, language: Literal["en", "ru"] = "ru"
    ) -> List[TextType]:
        endpoint = "intros" if language == "ru" else "intros_eng"
        response = await self._session.get_response(method="GET", endpoint=endpoint)
        return [TextType(*intro) for intro in response["intros"]]

    async def balaboba(self, query: str, text_type: Union[TextType, int], lang: Literal["en", "ru"] = 'ru') -> str:
        intro = text_type.number if isinstance(text_type, TextType) else text_type
        response = await self._session.get_response(
            method="POST",
            endpoint="text3",
            json={"query": query, "intro": intro, "filter": 1},
            headers=get_headers(query, intro, lang)
        )
        if 'type' in response and response['type'] == 'captcha':
            return f"CAPTCHA found!\n{response['captcha']['captcha-page']}"
        return "{}{}".format(response["query"], response["text"])
