import typing


def one_of_in(a: typing.Iterable, x: typing.Container | typing.Iterable):
    return any(map(lambda el: el in x, a))


def wrap(val: typing.Any) -> typing.Callable[[], typing.Any]:
    return lambda: val


def to_async(func):
    async def to_async_impl(*args, **kwargs):
        return func(*args, **kwargs)
    return to_async_impl


def to_int(val: typing.Any, default: int = 0) -> int:
    try:
        return int(val)
    except:
        return default


def to_float(val: typing.Any, default: float = 0) -> float:
    try:
        return float(val)
    except:
        return default


def indexed(a: typing.Iterable) -> typing.Iterable:
    return zip(a, range(len(a)))


def identity(x):
    return x


def values(a: list[tuple[int, typing.Any]]) -> list[typing.Any]:
    return [el[1] for el in a]

