import datetime
import typing
import utils.locale
import utils.numclass

translations = {
    'weeks': {
        'en': ['w', ('week', 'weeks')],
        'ru': ['нед', ('неделя', 'недели', 'недель')],
    },
    'days': {
        'en': ['d', ('day', 'days')],
        'ru': ['дн', ('день', 'дня', 'дней')],
    },
    'hours': {
        'en': ['h', ('hour', 'hours')],
        'ru': ['ч', ('час', 'часа', 'часов')],
    },
    'minutes': {
        'en': ['m', ('minute', 'minutes')],
        'ru': ['мин', ('минута', 'минуты', 'минут')],
    },
    'seconds': {
        'en': ['s', ('second', 'seconds')],
        'ru': ['сек', ('секунда', 'секунды', 'секунд')],
    },
    'milliseconds': {
        'en': ['ms', ('milliseconds',)],
        'ru': ['мс', ('миллисекунд',)],
    },
    'numclass': {
        'en': utils.numclass.one_many,
        'ru': utils.numclass.one_two_five,
    }
}
LOC = utils.locale.Localizator(translations)


def timedelta_to_str(d: datetime.timedelta, is_short: bool = False, lang: str = 'en') -> str:
    """
    15 weeks 4 days 10 hours 45 minutes 37 seconds 487.5 milliseconds, (is_short=False|default)
    15 недель 4 дня 10 часов 45 минут 37 секунд 487.5 миллисекунд
    15w 4d 10h 45m 37s 487.5ms, (is_short=True)
    15н 4д 10ч 45мин 37сек 487.5мс
    but no more than three highest
    """

    d = d + datetime.timedelta(microseconds=50)

    weeks, days = divmod(d.days, 7)
    minutes, seconds = divmod(d.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    ms = (d.microseconds // 100) / 10

    arr = [
        (weeks, 'weeks'),
        (days, 'days'),
        (hours, 'hours'),
        (minutes, 'minutes'),
        (seconds, 'seconds'),
        (ms, 'milliseconds')
    ]

    def is_not_null(el: typing.Tuple[int, str]) -> bool:
        cnt, _ = el
        return cnt != 0

    def short(val: int, name: str) -> str:
        form = LOC.obj(name, lang)[0]
        return f'{val}{form}'

    def long(val: int, name: str) -> str:
        forms = LOC.obj(name, lang)[1]
        form = forms[LOC.obj('numclass', lang)(val) if len(forms) != 1 else 0]
        return f'{val} {form}'

    def stringify(el: typing.Tuple[int, str]) -> str:
        cnt, name = el
        return short(cnt, name) if is_short else long(cnt, name)

    idx = 0
    while idx < len(arr) - 1 and not is_not_null(arr[idx]):
        idx += 1

    arr = arr[idx:idx + 3]
    arr = list(filter(is_not_null, arr))

    return ' '.join(map(stringify, arr))
