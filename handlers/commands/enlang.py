import utils.cm
import utils.ch
import utils.regex
import utils.str

import wn


handler_list = []
try:
    dic = wn.Wordnet('own-en')
except:
    wn.download('omw-en')
    dic = wn.Wordnet('omw-en')


async def define(cm: utils.cm.CommandMessage):
    if cm.arg:
        res = dic.synsets(cm.arg)
        if not res:
            await cm.int_cur.reply('word not found')
            return
        _arg = utils.str.escape(cm.arg)
        ss = [f"*{_arg}*"]
        for i, e in enumerate(res):
            _pos = utils.str.escape(e.pos)
            _def = utils.str.escape(e.definition()) 
            ss.append(f"{i+1}. _{_pos}_, {_def}")
        await cm.int_cur.reply('\n'.join(ss))


handler_list.append(
    utils.ch.CommandHandler(
        name='en_def',
        pattern=utils.regex.ignore_case(utils.regex.pat_starts_with(utils.regex.prefix() + utils.regex.unite('def', 'define'))),
        help_page=['define'],
        handler_impl=define,
        is_prefix=True
    )
)
