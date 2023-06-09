import utils.rand

import os
import typing
import pathlib


def list_files(path: str) -> list[str]:
    """
    list files in given folder
    https://stackoverflow.com/a/3207973
    """
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def list_filenames(path: str) -> list[str]:
    return [os.path.join(path, f) for f in list_files(path)]


def temp_filename() -> str:
    return f"/tmp/alterpy-{utils.rand.printable()}"


def is_file(path: str) -> bool:
    """return True if 'path' is a path to existing file (not folder)"""
    return pathlib.Path(path).is_file()


def create_dir(path: str) -> bool:
    try:
        os.mkdir(path)
    except FileExistsError:
        return False
    return True

