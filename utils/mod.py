import asyncio

import utils.log
import utils.file
import utils.common

import importlib

log = utils.log.get("modloader")


async def load_handlers_from_name(name: str) -> tuple[bool, list]:
    try:
        mod = importlib.import_module(name)
        mod = importlib.reload(mod)
        handlers = mod.handlers
        log.info(f"Loaded {name} OK!")
        return True, handlers
    except:
        log.exception(f"Failed to load handlers from {name}, ignoring module")
        return False, []


async def load_handlers_from_filename(filename: str) -> tuple[bool, list]:
    return await load_handlers_from_name(filename[:-3].replace('/', '.'))


async def load_handlers(initial_handlers: list, handlers: list, path: str) -> str:
    """
    load all .py files from given path and merge all of their "handlers" into given with initial
    returns log message
    """

    log.info(f"Started loading from {path}")

    if path[-1] != '/':
        path = path + '/'
    path = path.replace('\\', '/')

    handlers[:] = initial_handlers[:]
    filenames = list(filter(lambda fn: fn[-3:] == ".py", sorted(utils.file.list_filenames(path))))

    cnt_ok, cnt = 0, len(filenames)

    loaders = [load_handlers_from_filename(filename) for filename in filenames]
    for loader in asyncio.as_completed(loaders):
        ok, cur_handlers = await loader
        cnt_ok += int(ok)
        handlers.extend(cur_handlers)

    log.info(f"Loading from {path} finished, {cnt_ok} of {cnt} loaded successfully")

    return f"{cnt_ok} of {cnt} loaded successfully"

