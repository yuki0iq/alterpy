import typing

import util
import re


class RP1Handler(typing.NamedTuple):
    pattern: re.Pattern
    ans: typing.Callable[[], str]

    def invoke(self, user, comment):
        return self.ans().format(user, comment).strip()


class RP2Handler(typing.NamedTuple):
    pattern: re.Pattern
    ans: typing.Callable[[], str]

    def invoke(self, user, mention, comment):
        return self.ans().format(user, mention, comment).strip()


rp1handlers = [
    RP1Handler(re.compile(util.re_pat_starts_with("задолбало")), util.rand_or_null_fun("{0} успешно выпилился(ась) {1}", 1, 6, "{0} не смог(ла) выпилиться {1}"))
]

rp2handlers = [
    RP2Handler(re.compile(util.re_pat_starts_with("обнять")), util.wrap("{0} обнял(а) {1} {2}"))
]

mention_pattern = re.compile(r'''\[.+\]\(tg://user\?id=\d+\)|@\w+''')


async def on_rp(cm: util.CommandMessage):
    user = await cm.sender.get_mention()
    mention = (await cm.reply_sender.get_mention()) if cm.reply_sender is not None else "(nobody)"
    res = []
    for line in cm.arg.split('\n')[:20]:  # technical limitation
        # try match to RP-1 as "RP-1 arg"
        for handler in rp1handlers:
            match = re.search(handler.pattern, line)
            if match:
                arg = line[len(match[0]):]
                res.append(handler.invoke(user, arg))
        # try match to RP-2 as "RP-2 [mention] arg"
        for handler in rp2handlers:
            match = re.search(handler.pattern, line)
            if match:
                arg = line[len(match[0]):]
                cur_mention = mention
                match = re.search(mention_pattern, arg)
                if match:
                    cur_mention, arg = match[0], arg[len(match[0]):]
                res.append(handler.invoke(user, cur_mention, arg))
    if res:
        await cm.int_cur.reply('\n'.join(res))


handlers = [util.CommandHandler("role", re.compile(""), "Roleplay commands", "@yuki_the_girl", on_rp)]