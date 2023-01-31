import typing

import util
import re


class RP1Handler(typing.NamedTuple):
    pattern: re.Pattern
    ans: typing.Callable[[], str]
    ans_masc: typing.Callable[[], str]
    ans_fem: typing.Callable[[], str]

    def invoke(self, user, gender, comment):
        return [self.ans, self.ans_masc, self.ans_fem][gender]().format(user, comment).strip()


class RP2Handler(typing.NamedTuple):
    pattern: re.Pattern
    ans: typing.Callable[[], str]
    ans_masc: typing.Callable[[], str]
    ans_fem: typing.Callable[[], str]

    def invoke(self, user, gender, mention, comment):
        return [self.ans, self.ans_masc, self.ans_fem][gender]().format(user, mention, comment).strip()


rp1handlers = [
    RP1Handler(
        re.compile(util.re_pat_starts_with("задолбало")),
        util.rand_or_null_fun("{0} успешно выпилился(ась) {1}", 1, 6, "{0} не смог(ла) выпилиться {1}"),
        util.rand_or_null_fun("{0} успешно выпилился {1}", 1, 6, "{0} не смог выпилиться {1}"),
        util.rand_or_null_fun("{0} успешно выпилилась {1}", 1, 6, "{0} не смогла выпилиться {1}")
    )
]

rp2handlers = [
    RP2Handler(
        re.compile(util.re_pat_starts_with("обнять")),
        util.wrap("{0} обнял(а) {1} {2}"),
        util.wrap("{0} обнял {1} {2}"),
        util.wrap("{0} обняла {1} {2}")
    )
]

mention_pattern = re.compile(r'''\[.+\]\(tg://user\?id=\d+\)|@\w+''')


async def on_rp(cm: util.CommandMessage):
    user = await cm.sender.get_mention()
    gender = cm.sender.get_gender()
    mention = (await cm.reply_sender.get_mention()) if cm.reply_sender is not None else None
    res = []
    for line in cm.arg.split('\n')[:20]:  # technical limitation
        # try match to RP-1 as "RP-1 arg"
        for handler in rp1handlers:
            match = re.search(handler.pattern, line)
            if match:
                arg = line[len(match[0]):]
                res.append(handler.invoke(user, gender, arg))
        # try match to RP-2 as "RP-2 [mention] arg"
        for handler in rp2handlers:
            match = re.search(handler.pattern, line)
            if match:
                arg = line[len(match[0]):]
                cur_mention = mention
                match = re.search(mention_pattern, arg)
                if match:
                    cur_mention, arg = match[0], arg[len(match[0]):]
                    # FIX cur_mention IFF id is specified
                if cur_mention is not None:
                    res.append(handler.invoke(user, gender, cur_mention, arg))
                else:
                    res.append("RP-2 commands can't be executed without second user mention")
    if res:
        await cm.int_cur.reply('\n'.join(res))


handlers = [util.CommandHandler("role", re.compile(""), "Roleplay commands", "@yuki_the_girl", on_rp)]