import utils.common
import iuliia


def inflector(s, _):
    return utils.common.wrap


def agree_with_number(s, num, _):
    if type(num) != int or abs(num) > 1:
        return s + "s"
    return s


def tr(s):
    return iuliia.translate(s, iuliia.WIKIPEDIA)
