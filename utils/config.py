import pytomlpp
import typing
import os


def to_path(name: str) -> str:
    return f"./config/{name}.toml"


def load(name: str) -> typing.Dict[typing.Any, typing.Any]:
    """get config by filename"""
    path = to_path(name)
    if not os.path.exists(path):
        with open(path, "w") as f:
            pass
    return pytomlpp.load(path)


def save(name: str, conf: typing.Dict[typing.Any, typing.Any]) -> None:
    """save config by filename"""
    pytomlpp.dump(conf, to_path(name))

