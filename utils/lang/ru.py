import pymorphy3
import utils.pyphrasy3
import utils.str
import utils.log
import utils.transliterator
import utils.kiri43i
import spacy


log = utils.log.get("lang-ru")

spacy_model_name = "ru_core_news_md"
log.info("Probing spaCy-ru...")
try:
    nlp = spacy.load(spacy_model_name)
except OSError:
    log.info("Model not found, downloading...")
    import spacy.cli.download
    spacy.cli.download(spacy_model_name)
    nlp = spacy.load(spacy_model_name)
log.info("spaCy-ru OK!")


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
