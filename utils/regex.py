import re


def pat_starts_with(s: str) -> str:
    """
    wrap regex pattern into "Case insensitive; Starts with and ends with whitespace or end of string"
    """
    return f"^({s})($|\\s)"


def ignore_case(pat: str) -> re.Pattern:
    return re.compile(f"(?i)({pat})")


def only_prefix() -> str:
    """regex pattern for command prefix"""
    return unite('/', '\\!', '•', '\\.', 'альтер', '_', '#') + "\\s*"


def prefix() -> str:
    """regex pattern for optional prefix"""
    return optional(only_prefix())


def union(a) -> str:
    return '(' + '|'.join(map(str, a)) + ')'


def unite(*args) -> str:
    return union(args)


def optional(a: str) -> str:
    return f"({a})?"


def raw_command(a: str) -> re.Pattern:
    return ignore_case(pat_starts_with(a))


def command(a: str) -> re.Pattern:
    return raw_command(prefix() + a)


def pre_command(a: str) -> re.Pattern:
    return raw_command(only_prefix() + a)