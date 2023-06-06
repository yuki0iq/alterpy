import pytomlpp
import typing
import os


def load(name: str) -> typing.Dict[typing.Any, typing.Any]:
    """get config by filename"""
    if not os.path.exists(name):
        f = open(name, "w")
        f.close()
    return pytomlpp.load(name)


def save(name: str, conf: typing.Dict[typing.Any, typing.Any]) -> None:
    """save config by filename"""
    pytomlpp.dump(conf, name)

