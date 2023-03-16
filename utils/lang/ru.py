import pymorphy3
import utils.pyphrasy3
import utils.str
import utils.transliterator
import utils.kiri43i


class MorphAnalyzer:
    __slots__ = ['morph']

    def __init__(self, morph):
        self.morph = morph

    def parse(self, word):
        return [el._replace(word=utils.str.equal_capitalize(el.word, word)) for el in self.morph.parse(word)]


def parse_inflect(word, form):
    if type(form) == str:
        form = {form}
    res = word.inflect(form)
    return res._replace(word=utils.str.equal_capitalize(res.word, word.word))


morph = MorphAnalyzer(pymorphy3.MorphAnalyzer())
pi = utils.pyphrasy3.PhraseInflector(morph, parse_inflect)


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
