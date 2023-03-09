import pymorphy3
import utils.pyphrasy3

morph = pymorphy3.MorphAnalyzer()
pi = utils.pyphrasy3.PhraseInflector(morph)


def inflector(form):
    return lambda s: pi.inflect(s, form)


def agree_with_number(s, num, form):
    return morph.parse(s)[0].inflect(form).make_agree_with_number(num).word
