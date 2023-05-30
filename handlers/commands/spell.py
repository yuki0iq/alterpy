import utils.cm
import utils.ch
import utils.log
import utils.regex
import utils.str
import context

import utils.aiospeller

handler_list = []


async def spell(cm: utils.cm.CommandMessage):
    if cm.arg:
        await cm.int_cur.reply(utils.str.escape(await utils.aiospeller.correct(context.session, cm.arg)))


handler_list.append(
    utils.ch.CommandHandler(
        name='speller',
        pattern=utils.regex.cmd(utils.regex.unite('typo', 'исправь')),
        help_page='speller',
        handler_impl=spell,
        is_prefix=True
    )
)
