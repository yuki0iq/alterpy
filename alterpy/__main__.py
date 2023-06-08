import utils.log
import asyncio
import rich.traceback

from . import core


log = utils.log.get("main")

rich.traceback.install(show_locals=True)
try:
    asyncio.run(core.main(log))
except KeyboardInterrupt:
    log.info("Stopping... [KeyboardInterrupt]")

