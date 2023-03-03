import utils


def to_str_ru(pronoun_set: int) -> str:
    return ["нейтральный", "он/его", "она/её"][pronoun_set]


def to_str_en(pronoun_set: int) -> str:
    return ["neutral they/them/themself", "he/him", "she/her"][pronoun_set]


def from_str(s: str) -> int:
    s = s.lower()
    if utils.common.one_of_in(["they", "them", "themsel", "оно", "они"], s):
        return 0
    if utils.common.one_of_in(["fem", "wom", "жен", "дев", "фем", "gi", "she", "her", "она"], s) or s in list('2fжд'):
        return 2
    if utils.common.one_of_in(["mas", "mal", "муж", "пар", "мас", "gu", "he", "him", "his", "он"], s) or s in list('1mмп'):
        return 1
    return 0
