import pytomlpp
import logging
import traceback
import time


def get_config(name):
    """get config by filename"""
    return pytomlpp.load(name)


def set_config(name, conf):
    """save config by filename"""
    pytomlpp.dump(conf, name)



logging_formatter = logging.Formatter("%(asctime)s: %(name)s [%(levelname)s]:  %(message)s")
logging.basicConfig(format="%(asctime)s: %(name)s [%(levelname)s]:  %(message)s", level=logging.DEBUG)

def get_log(name="unknown"):
    '''create log with given name'''
    log = logging.getLogger(name)
    # TODO log.setLevel(logging.DEBUG if bot_debug else logging.INFO)
    log.setLevel(logging.DEBUG)

    ti = time.ctime().replace(":", " ").replace("  ", " ")
    ti = ti.split(" ")
    ti = "_".join(ti[1:3])

    h_file = logging.FileHandler(f"log/logs_{ti}.log", encoding="utf-8")
    h_file.setFormatter(logging_formatter)
    log.addHandler(h_file)
    # log.addHandler(logging_handler_stderr)

    return log

def log_fail(log, text):
    log.error(f"{text}\n{traceback.format_exc()}")
