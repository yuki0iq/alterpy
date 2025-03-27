import asyncio
import rich.console
import rich.traceback
import sys
import utils.log

from . import core


log = utils.log.get("main")

rich.traceback.install(show_locals=True)

try:
    asyncio.run(core.main(log))
except KeyboardInterrupt:
    log.info("Stopping... [KeyboardInterrupt]")
except SystemExit:
    log.info("Shutting down...")
