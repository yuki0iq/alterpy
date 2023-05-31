import utils.common
import utils.log
import iuliia
import lemminflect
import wn


log = utils.log.get("lang-en")

log.info("Probing WordNet-en")
try:
    dic = wn.Wordnet('own-en')
except:
    log.info("Not found, downloading...")
    wn.download('omw-en')
    dic = wn.Wordnet('omw-en')
log.info("WordNet-en OK!")


def _pos(s: str):
    ans = set()
    for el in dic.synsets(s):
        ans.add(el.pos)
    return ans


def try_verb_past(w: str, p: int):
    return inflect(w, 'VBD') if 'v' in _pos(w) else w


def inflect(s, form):
    return lemminflect.getInflection(s, form)[0]


def inflector(form):
    return lambda s: inflect(s, form)


def agree_with_number(s, num, _):
    if type(num) != int or abs(num) > 1:
        return s + "s"
    return s


def tr(s):
    return iuliia.translate(s, iuliia.WIKIPEDIA)

