import logging
import rich.logging


logging_formatter = logging.Formatter("%(asctime)s: %(name)s [%(levelname)s]:  %(message)s")
logging.basicConfig(
    format="%(name)s:  %(message)s",
    level=logging.INFO,
    handlers=[rich.logging.RichHandler(
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        markup=True,
        log_time_format="%Y-%m-%d, %H:%M:%S"
    )]
)


def get(name:str = "unknown") -> logging.Logger:
    """create log with given name"""
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)

    h_file = logging.FileHandler("/dev/null", encoding="utf-8")
    h_file.setFormatter(logging_formatter)
    log.addHandler(h_file)
    # log.addHandler(logging_handler_stderr)

    return log

