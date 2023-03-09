import utils.str
import importlib


class Localizator:
    __slots__ = ['d']

    def __init__(self, d):
        self.d = d

    def obj(self, s: str, lang: str):
        if s not in self.d:
            return None
        cur = self.d[s]
        if type(cur) == str:
            return cur
        if not cur:
            return None
        return cur[lang] if lang in cur else list(cur)[0]

    def get(self, s: str, lang: str) -> str:
        return str(utils.str.FStr(self.obj(s, lang)))


def lang(lg: str):
    mod = importlib.import_module(f"utils.lang.{lg}")
    return mod
