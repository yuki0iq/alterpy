import re
import typing


def pat_starts_with(s: str) -> str:
    """
    wrap regex pattern into "Case insensitive; Starts with and ends with whitespace or end of string"
    """
    return f"^({s})($|\\s)"


def ignore_case(pat: str) -> re.Pattern[str]:
    return re.compile(f"(?i)({pat})")


def only_prefix() -> str:
    """regex pattern for command prefix"""
    return unite('/', '\\!', '•', '\\.', 'альтер', '_', '#') + "\\s*"


def prefix() -> str:
    """regex pattern for optional prefix"""
    return optional(only_prefix())


def union(a: typing.Iterable[typing.Any]) -> str:
    return '(' + '|'.join(map(str, a)) + ')'


def unite(*args: typing.Any) -> str:
    return union(args)


def optional(a: str) -> str:
    return f"({a})?"


def raw(a: str) -> re.Pattern[str]:
    return ignore_case(pat_starts_with(a))


def cmd(a: str) -> re.Pattern[str]:
    return raw(prefix() + a)


def pre(a: str) -> re.Pattern[str]:
    return raw(only_prefix() + a)


def add(a: str) -> re.Pattern[str]:
    return raw(r'\+' + a)


def sub(a: str) -> re.Pattern[str]:
    return raw('-' + a)


def ask(a: str) -> re.Pattern[str]:
    return raw(r'\?' + a)


def word_border() -> str:
    return r'\b'


def split_by_word_border(a: str) -> list[str]:
    return re.split(word_border(), a)


def negative_lookbehind(a: str) -> str:
    return f'(?<!{a})'


def negative_lookahead(a: str) -> str:
    return f'(?!{a})'


def named(name: str, pat: str) -> str:
    return f"(?P<{name}>({pat}))"


def integer() -> str:
    return "[1-9]\\d*"


def named_int(name: str) -> str:
    return named(name, integer())
