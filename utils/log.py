import logging
import rich.logging


logging_formatter = logging.Formatter("%(asctime)s: %(name)s [%(levelname)s]:  %(message)s")
logging.basicConfig(
    format="%(name)s:  %(message)s",
    level=logging.INFO,
    handlers=[rich.logging.RichHandler(rich_tracebacks=True, tracebacks_show_locals=True, markup=True)]
)


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

