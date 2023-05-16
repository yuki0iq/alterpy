import typing


def one_of_in(a: typing.Iterable, x: typing.Container | typing.Iterable):
    return any(map(lambda el: el in x, a))


def wrap(val: typing.Any) -> typing.Callable[[], typing.Any]:
    return lambda: val


def starts_with(greater, lesser):
    return len(lesser) <= len(greater) and all(x == y for x, y in zip(lesser, greater))

def to_async(func):
    async def to_async_impl(*args, **kwargs):
        return func(*args, **kwargs)
    return to_async_impl


def to_int(val: typing.Any, default: int = 0) -> int:
    try:
        return int(val)
    except ValueError:
        return default


def to_float(val: typing.Any, default: float = 0) -> float:
    try:
        return float(val)
    except ValueError:
        return default


def identity(x):
    return x


def values(a: list[tuple[int, typing.Any]]) -> list[typing.Any]:
    return [el[1] for el in a]


def split_by_func(s: str, f: callable) -> list[str]:
    res = []
    cur = []
    p = s[0]
    for c in s:
        if f(c) != f(p):
            res.append(''.join(cur))
            cur = []
        cur.append(c)
        p = c
    res.append(''.join(cur))
    return res

