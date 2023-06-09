import pymorphy3
import utils.pyphrasy3
import utils.str
import utils.log
import utils.transliterator
import utils.kiri43i
import os.path
import typing

log = utils.log.get("lang-ru")


class MorphAnalyzer:
    __slots__ = ['morph']

    def __init__(self, morph: pymorphy3.MorphAnalyzer) -> None:
        self.morph = morph

    def parse(self, word: str) -> list[pymorphy3.analyzer.Parse]:
        def make_equal(x: str) -> str:
            return utils.str.equal_capitalize(x, word)

        return [
            el._replace(
                word=make_equal(el.word),
                normal_form=make_equal(el.normal_form)
            )
            for el in self.morph.parse(word)
        ]


def parse_inflect(word: pymorphy3.analyzer.Parse, form: typing.Union[str, set[str], frozenset[str]]) -> pymorphy3.analyzer.Parse:
    if type(form) == str:
        form = {form}
    res = word.inflect(form)
    return res._replace(word=utils.str.equal_capitalize(res.word, word.word))


def word_inflect_parse(word: str, form: typing.Union[str, set[str], frozenset[str]]) -> pymorphy3.analyzer.Parse:
    return parse_inflect(morph.parse(word)[0], form)


def word_inflect(word: str, form: typing.Union[str, set[str], frozenset[str]]) -> str:
    ret = word_inflect_parse(word, form).word
    assert isinstance(ret, str)
    return ret


def parse_inflect_word(word: pymorphy3.analyzer.Parse, form: typing.Union[str, set[str], frozenset[str]]) -> str:
    ret = parse_inflect(word, form).word
    assert isinstance(ret, str)
    return ret


morph = MorphAnalyzer(pymorphy3.MorphAnalyzer())
pi = utils.pyphrasy3.PhraseInflector(morph, parse_inflect)


def merge(a: str, b: str) -> str:
    return f'{a}({b[len(os.path.commonprefix([a, b])):]})'


pasts = [frozenset({'past', 'sing', 'masc'}), frozenset({'past', 'sing', 'femn'}), frozenset({'past', 'sing', 'neut'}), frozenset({'past', 'plur'})]
pn_to_pi = [0, 0, 1, 2, 2, 3]

def _past(parse: pymorphy3.analyzer.Parse, i: int) -> str:
    return parse_inflect_word(parse, pasts[i])


def past(parse: pymorphy3.analyzer.Parse, p: int) -> str:
    if p == 0: return merge(_past(parse, 0), _past(parse, 1))
    return _past(parse, pn_to_pi[p])


def try_verb_past(w: str, p: int) -> str:
    parse = morph.parse(w)[0]
    tag = parse.tag
    if 'INFN' not in tag:
        return w
    return past(parse, p)


def inflect(s: str, form: typing.Union[str, set[str], frozenset[str]]) -> str:
    try:
        return pi.inflect(s, form)
    except:
        return word_inflect(s, form)


def inflector(form: typing.Union[str, set[str], frozenset[str]]) -> typing.Callable[[str], str]:
    return lambda s: inflect(s, form)


def agree_with_number(s: str, num: int, form: typing.Union[str, set[str], frozenset[str]]) -> str:
    ret = word_inflect_parse(s, form).make_agree_with_number(num).word
    assert isinstance(ret, str)
    return ret


translit = utils.transliterator.Transliterator()


def tr(s: str) -> str:
    return translit.inverse_transliterate(utils.kiri43i.parse(s))


def ander(arr: list[str]) -> str:
    return (', '.join(arr))[::-1].replace(' ,', ' и ', 1)[::-1]

