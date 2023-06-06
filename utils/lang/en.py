import utils.common
import utils.log
import iuliia
import lemminflect
import wn
import typing


log = utils.log.get("lang-en")

log.info("Probing WordNet-en")
try:
    dic = wn.Wordnet('own-en')
except:
    log.info("Not found, downloading...")
    wn.download('omw-en')
    dic = wn.Wordnet('omw-en')
log.info("WordNet-en OK!")


def _pos(s: str) -> set[str]:
    ans = set()
    for el in dic.synsets(s):
        ans.add(el.pos)
    return ans


def try_verb_past(w: str, p: int) -> str:
    return inflect(w, 'VBD') if 'v' in _pos(w) else w


def inflect(s: str, form: str) -> str:
    return lemminflect.getInflection(s, form)[0]


def inflector(form: str) -> typing.Callable[[str], str]:
    return lambda s: inflect(s, form)


def agree_with_number(s: str, num: int, _: typing.Any) -> str:
    if type(num) != int or abs(num) > 1:
        return s + "s"
    return s


def tr(s: str) -> str:
    return iuliia.translate(s, iuliia.WIKIPEDIA)

