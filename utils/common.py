import typing


def one_of_in(a: typing.Iterable[typing.Any], x: typing.Container[typing.Any]) -> bool:
    return any(map(lambda el: el in x, a))


def wrap(val: typing.Any) -> typing.Callable[[], typing.Any]:
    return lambda: val


def starts_with(greater: str, lesser: str) -> bool:
    return len(lesser) <= len(greater) and all(x == y for x, y in zip(lesser, greater))

def to_async(func: typing.Callable[..., typing.Any]) -> typing.Callable[..., typing.Awaitable[typing.Any]]:
    async def to_async_impl(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
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


def identity(x: typing.Any) -> typing.Any:
    return x


def split_by_func(s: str, f: typing.Callable[[str], bool]) -> list[str]:
    res = []
    cur: list[str] = []
    p = s[0]
    for c in s:
        if f(c) != f(p):
            res.append(''.join(cur))
            cur = []
        cur.append(c)
        p = c
    res.append(''.join(cur))
    return res

