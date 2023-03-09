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


class FStr:
    __slots__ = ['_s']

    def __init__(self, s):
        self._s = s

    def __repr__(self):
        return eval(str(self))

    def __str__(self):
        return f"""f'''{self._s}'''"""
