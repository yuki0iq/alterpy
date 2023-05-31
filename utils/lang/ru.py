import pymorphy3
import utils.pyphrasy3
import utils.str
import utils.log
import utils.transliterator
import utils.kiri43i


log = utils.log.get("lang-ru")


class MorphAnalyzer:
    __slots__ = ['morph']

    def __init__(self, morph):
        self.morph = morph

    def parse(self, word):
        E = lambda x: utils.str.equal_capitalize(x, word)
        return [el._replace(word=E(el.word), normal_form=E(el.normal_form)) for el in self.morph.parse(word)]


def parse_inflect(word, form):
    if type(form) == str:
        form = {form}
    res = word.inflect(form)
    return res._replace(word=utils.str.equal_capitalize(res.word, word.word))


morph = MorphAnalyzer(pymorphy3.MorphAnalyzer())
pi = utils.pyphrasy3.PhraseInflector(morph, parse_inflect)


def merge(a, b):
    a, b = a(), b()
    res = []
    i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]:
        res.append(a[i])
    res.extend([a[i:], '(', b[i:], ')'])
    return ''.join(res)


def past(parse, p: int):
    masc = lambda: parse_inflect(parse, {'past', 'sing', 'masc'}).word
    femn = lambda: parse_inflect(parse, {'past', 'sing', 'femn'}).word
    neut = lambda: parse_inflect(parse, {'past', 'sing', 'neut'}).word
    plur = lambda: parse_inflect(parse, {'past', 'plur'}).word
    _neu = lambda: merge(masc, femn)
    return [_neu, masc, femn, neut, neut, plur][p]()


def try_verb_past(w: str, p: int):
    parse = morph.parse(w)[0]
    tag = parse.tag
    if 'INFN' not in tag:
        return w
    return past(parse, p)
    return parse_inflect(parse, {'past', 'plur'}).word  # TODO respect pronouns!!


def inflect(s, form):
    try:
        return pi.inflect(s, form)
    except:
        return parse_inflect(morph.parse(s)[0], form).word


def inflector(form):
    return lambda s: inflect(s, form)


def agree_with_number(s, num, form):
    return morph.parse(s)[0].inflect(form).make_agree_with_number(num).word


translit = utils.transliterator.Transliterator()


def tr(s):
    return translit.inverse_transliterate(utils.kiri43i.parse(s))


def ander(arr: [str]) -> str:
    return (', '.join(arr))[::-1].replace(' ,', ' и ', 1)[::-1]
