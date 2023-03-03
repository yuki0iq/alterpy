import logging
import traceback


logging_formatter = logging.Formatter("%(asctime)s: %(name)s [%(levelname)s]:  %(message)s")
logging.basicConfig(format="%(asctime)s: %(name)s [%(levelname)s]:  %(message)s", level=logging.INFO)


def get(name="unknown") -> logging.Logger:
    """create log with given name"""
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)

    # ti = time.ctime().replace(":", " ").replace("  ", " ")
    # ti = ti.split(" ")
    # ti = "_".join(ti[1:3])

    h_file = logging.FileHandler(f"log/{name}.log", encoding="utf-8")
    h_file.setFormatter(logging_formatter)
    log.addHandler(h_file)
    # log.addHandler(logging_handler_stderr)

    return log


def fail(log: logging.Logger, text: str) -> None:
    log.error(f"{text}\n{traceback.format_exc()}")
