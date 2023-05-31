import utils.str
import utils.lang.ru, utils.lang.en


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


langs = {
    'ru': utils.lang.ru,
    'en': utils.lang.en,
}


def lang(lg: str):
    return langs[lg]


def detect(s: str):
    if not s: return 'en'
    if 'а' <= s[0].lower() <= 'я': return 'ru'
    if 'a' <= s[0].lower() <= 'z': return 'en'
    return 'en'  # lmao


def try_verb_past(w: str, p: int):
    return lang(detect(w)).try_verb_past(w, p)

