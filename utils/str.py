import unicodedata
import utils.common
import urllib.parse


def change_layout(s: str) -> str:
    """alternate between QWERTY and JCUKEN"""
    en = r"""`~!@#$^&qwertyuiop[]\QWERTYUIOP{}|asdfghjkl;'ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>?"""
    ru = r"""ёЁ!"№;:?йцукенгшщзхъ\ЙЦУКЕНГШЩЗХЪ/фывапролджэФЫВАПРОЛДЖЭячсмитьбю.ЯЧСМИТЬБЮ,"""
    fr, to = en + ru, ru + en

    res = []
    for c in s:
        if c in fr:
            res.append(to[fr.index(c)])
        else:
            res.append(c)
    return ''.join(res)


def is_eng(s: str) -> bool:
    return not s or 'a' <= s[0].lower() <= 'z'


def equal_capitalize(word: str, pattern: str) -> str:
    def pat(idx: int):
        if idx >= len(pattern):
            return pattern[-1].islower()
        return pattern[idx].islower()

    word = list(word)
    for i in range(len(word)):
        word[i] = word[i].lower() if pat(i) else word[i].upper()
    return ''.join(word)


class FStr:
    __slots__ = ['_s']

    def __init__(self, s):
        self._s = s

    def __repr__(self):
        return eval(str(self))

    def __str__(self):
        return f"""f'''{self._s}'''"""


def is_full(ch: str) -> bool:
    return unicodedata.east_asian_width(ch) in ['F', 'W']


def is_kanji(ch: str) -> bool:
    return utils.common.one_of_in(['HIRAGANA', 'KATAKANA', 'CJK'], unicodedata.name(ch[0]))


def strlen(s: str) -> int:
    return sum(2 if is_full(ch) else 1 for ch in s)


def is_normal_space(ch: str) -> bool:
    return ch in '\t\n\x0b\x0c\r '


def rjust(s: str, n: int) -> str:
    """Fullwidth-aware right justify"""
    return s.rjust(n - (strlen(s) - len(s)))


def escape(s: str) -> str:
    return s.replace('\\', '\\\\').replace('_', r'\_').replace('[', r'\[').replace(']', r'\]').replace('*', r'\*').replace('`', r'\`')


def urlencode(s: str) -> str:
    return urllib.parse.quote(s)

