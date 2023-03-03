import utils.log
import utils.file
import utils.common

import importlib

log = utils.log.get("modular")


def load_handlers(initial_handlers: list, handlers: list, path: str) -> list[str]:
    """
    load all .py files from given path and merge all of their "handlers" into given with initial
    returns log message
    """

    if path[-1] != '/':
        path = path + '/'
    path = path.replace('\\', '/')
    base = path.replace('/', '.')

    handlers[:] = initial_handlers[:]
    filenames = list(filter(lambda fn: fn[-3:] == ".py", sorted(utils.file.list_files(path))))

    cnt_ok, cnt, res = 0, len(filenames), []

    for filename, idx in utils.common.indexed(filenames):
        try:
            name = base + filename[:-3]
            mod = importlib.import_module(name)
            mod = importlib.reload(mod)
            handlers.extend(mod.handlers)

            cnt_ok += 1
            res.append(f"({idx+1:03}/{cnt:03}) <  OK  >  `{name}`")
        except:
            utils.log.fail(log, f"Loading {path}{filename} failed")
            res.append(f"({idx+1:03}/{cnt:03}) <failed>  `{name}`")

    res.append(f"--> {cnt_ok:03} of {cnt:03} loaded successfully!")

    return res
