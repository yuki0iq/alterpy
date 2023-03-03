import datetime
import typing


def timedelta_to_str(d: datetime.timedelta, is_short: bool = False) -> str:
    """
    15 weeks 4 days 10 hours 45 minutes 37 seconds 487.5 milliseconds, (is_short=False|default)
    15w 4d 10h 45m 37s 487.5ms, (is_short=True)
    but no more than three highest
    """

    d = d + datetime.timedelta(microseconds=50)

    weeks, days = divmod(d.days, 7)
    minutes, seconds = divmod(d.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    ms = (d.microseconds // 100) / 10

    arr = [
        (weeks, 'w', 'weeks'),
        (days, 'd', 'days'),
        (hours, 'h', 'hours'),
        (minutes, 'm', 'minutes'),
        (seconds, 's', 'seconds'),
        (ms, 'ms', 'milliseconds')
    ]

    def is_not_null(el: typing.Tuple[int, str, str]) -> bool:
        cnt, _, _ = el
        return cnt != 0

    def stringify(el: typing.Tuple[int, str, str]) -> str:
        cnt, short_name, name = el
        return f"{cnt}{short_name}" if is_short else f"{cnt} {name}"

    idx = 0
    while idx < len(arr) - 1 and not is_not_null(arr[idx]):
        idx += 1

    arr = arr[idx:idx + 3]
    arr = list(filter(is_not_null, arr))

    return ' '.join(map(stringify, arr))