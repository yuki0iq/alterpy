import utils.common
import utils.log
import iuliia
import lemminflect
import typing


def try_verb_past(w: str, p: int) -> str:
    return inflect(w, 'VBD')


def inflect(s: str, form: str) -> str:
    ret = lemminflect.getInflection(s, form)[0]
    assert isinstance(ret, str)
    return ret


def inflector(form: str) -> typing.Callable[[str], str]:
    return lambda s: inflect(s, form)


def agree_with_number(s: str, num: int, _: typing.Any) -> str:
    if type(num) != int or abs(num) > 1:
        return s + "s"
    return s


def tr(s: str) -> str:
    ret = iuliia.translate(s, iuliia.WIKIPEDIA)
    assert isinstance(ret, str)
    return ret

