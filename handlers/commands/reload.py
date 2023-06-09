import utils.cm
import utils.mod
import utils.ch
import utils.regex
import utils.system
import handlers.cm
import os
import sys
import PyGitUp.gitup


async def on_reload(cm: utils.cm.CommandMessage) -> None:
    res = await utils.mod.load_handlers(
        handlers.cm.initial_handlers,
        handlers.cm.ch_list,
        handlers.cm.handlers_dir,
        True
    )
    await cm.int_cur.reply(res)


async def on_hard_reload(cm: utils.cm.CommandMessage) -> None:
    # TODO: other way/
    with open('restarter.txt', 'w') as f:
        print(cm.sender.chat_id, cm.id, file=f)
    PyGitUp.gitup.GitUp().run()
    await cm.int_cur.reply('→ Restarting...')
    argv = utils.system.argv()
    os.execv(sys.executable, argv)


handler_list = [
    utils.ch.CommandHandler(name="reload", pattern=utils.regex.cmd(utils.regex.unite("перезапуск", "reload")), help_page='elevated', handler_impl=on_reload, is_elevated=True),
    utils.ch.CommandHandler(name="reload", pattern=utils.regex.cmd(utils.regex.unite("рестарт", "reboot")), help_page='elevated', handler_impl=on_hard_reload, is_elevated=True),
]

