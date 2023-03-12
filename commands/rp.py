import utils.ch
import utils.cm
import utils.regex
import utils.rand
import utils.common
import utils.locale
import utils.user

import typing
import re


def inflect_mention(mention: str, form: str, lang: str = "ru") -> str:
    if not mention:
        return mention
    le, ri = 1, mention.rindex(']')
    return mention[:le] + utils.locale.lang(lang).inflect(mention[le:ri], form) + mention[ri:]


class RP1Handler(typing.NamedTuple):
    pattern: re.Pattern
    ans: typing.Callable[[], str]
    ans_masc: typing.Callable[[], str]
    ans_fem: typing.Callable[[], str]

    def invoke(self, user, pronouns, comment):
        return [self.ans, self.ans_masc, self.ans_fem][pronouns]().format(user, comment).strip()


class RP2Handler(typing.NamedTuple):
    pattern: re.Pattern
    ans: typing.Callable[[], str]
    ans_masc: typing.Callable[[], str]
    ans_fem: typing.Callable[[], str]
    lang: str = "ru"
    form: str = "accs"

    def invoke(self, user, pronouns, mention, comment):
        return [self.ans, self.ans_masc, self.ans_fem][pronouns]().format(
            user, inflect_mention(mention, self.form, self.lang), comment
        ).strip().replace('  ', ' ', 1)


rp1handlers = [
    RP1Handler(
        utils.regex.command("задолбало"),
        utils.rand.rand_or_null_fun("😭 | {0} успешно выпилился(ась) {1}", 1, 6, "🎉 | {0} не смог(ла) выпилиться {1}"),
        utils.rand.rand_or_null_fun("😭 | {0} успешно выпилился {1}", 1, 6, "🎉 | {0} не смог выпилиться {1}"),
        utils.rand.rand_or_null_fun("😭 | {0} успешно выпилилась {1}", 1, 6, "🎉 | {0} не смогла выпилиться {1}")
    )
]

rp2handlers = [
    RP2Handler(
        utils.regex.command("обнять"),
        utils.common.wrap("🤗 | {0} обнял(а) {1} {2}"),
        utils.common.wrap("🤗 | {0} обнял {1} {2}"),
        utils.common.wrap("🤗 | {0} обняла {1} {2}")
    ),
    RP2Handler(
        utils.regex.command("дать"),
        utils.common.wrap("🎁 | {0} дал(а) {1} {2}"),
        utils.common.wrap("🎁 | {0} дал {1} {2}"),
        utils.common.wrap("🎁 | {0} дала {1} {2}"),
        form="datv",
    ),
    RP2Handler(
        utils.regex.command("сломать"),
        utils.common.wrap("🔧 | {0} сломал(а) {1} {2}"),
        utils.common.wrap("🔧 | {0} сломал {1} {2}"),
        utils.common.wrap("🔧 | {0} сломала {1} {2}"),
    ),
    RP2Handler(
        utils.regex.command("убить"),
        utils.common.wrap("☠ | {0} убил(а) {1} {2}"),
        utils.common.wrap("☠ | {0} убил {1} {2}"),
        utils.common.wrap("☠ | {0} убила {1} {2}")
    ),
    RP2Handler(
        utils.regex.command("расстрелять"),
        utils.common.wrap("🔫 | {0} расстрелял(а) {1} {2}"),
        utils.common.wrap("🔫 | {0} расстрелял {1} {2}"),
        utils.common.wrap("🔫 | {0} расстреляла {1} {2}")
    ),
    RP2Handler(
        utils.regex.command("поцеловать"),
        utils.common.wrap("😘 | {0} поцеловал(а) {1} {2}"),
        utils.common.wrap("😘 | {0} поцеловал {1} {2}"),
        utils.common.wrap("😘 | {0} поцеловала {1} {2}")
    ),
    RP2Handler(
        utils.regex.command("кусь(нуть){0,1}|укусить"),
        utils.common.wrap("😬 | {0} кусьнул(а) {1} {2}"),
        utils.common.wrap("😬 | {0} кусьнул {1} {2}"),
        utils.common.wrap("😬 | {0} кусьнула {1} {2}")
    ),
    RP2Handler(
        utils.regex.command("пнуть"),
        utils.common.wrap("👞 | {0} пнул(а) {1} {2}"),
        utils.common.wrap("👞 | {0} пнул {1} {2}"),
        utils.common.wrap("👞 | {0} пнула {1} {2}")
    ),
    RP2Handler(
        utils.regex.command("прижать"),
        utils.common.wrap("🤲 | {0} прижал(а) {1} {2}"),
        utils.common.wrap("🤲 | {0} прижал {1} {2}"),
        utils.common.wrap("🤲 | {0} прижала {1} {2}")
    ),
    RP2Handler(
        utils.regex.command("погладить"),
        utils.common.wrap("🤲 | {0} погладил(а) {1} {2}"),
        utils.common.wrap("🤲 | {0} погладил {1} {2}"),
        utils.common.wrap("🤲 | {0} погладила {1} {2}")
    ),
    RP2Handler(
        utils.regex.command("потрогать"),
        utils.common.wrap("🙌 | {0} потрогал(а) {1} {2}"),
        utils.common.wrap("🙌 | {0} потрогал {1} {2}"),
        utils.common.wrap("🙌 | {0} потрогала {1} {2}")
    ),
    RP2Handler(
        utils.regex.command("лизнуть"),
        utils.common.wrap("👅 | {0} лизнул(а) {1} {2}"),
        utils.common.wrap("👅 | {0} лизнул {1} {2}"),
        utils.common.wrap("👅 | {0} лизнула {1} {2}")
    ),
    RP2Handler(
        utils.regex.command("понюхать"),
        utils.common.wrap("👃 | {0} понюхал(а) {1} {2}"),
        utils.common.wrap("👃 | {0} понюхал {1} {2}"),
        utils.common.wrap("👃 | {0} понюхала {1} {2}")
    ),
    RP2Handler(
        utils.regex.command("ударить"),
        utils.common.wrap("🤜😵 | {0} ударил(а) {1} {2}"),
        utils.common.wrap("🤜😵 | {0} ударил {1} {2}"),
        utils.common.wrap("🤜😵 | {0} ударила {1} {2}")
    ),
    RP2Handler(
        utils.regex.command("шлепнуть"),
        utils.common.wrap("👏 | {0} шлепнул(а) {1} {2}"),
        utils.common.wrap("👏 | {0} шлепнул {1} {2}"),
        utils.common.wrap("👏 | {0} шлепнула {1} {2}")
    ),
    RP2Handler(
        utils.regex.command("шлёпнуть"),
        utils.common.wrap("👏 | {0} шлёпнул(а) {1} {2}"),
        utils.common.wrap("👏 | {0} шлёпнул {1} {2}"),
        utils.common.wrap("👏 | {0} шлёпнула {1} {2}")
    ),
    RP2Handler(
        utils.regex.command("предложить пива"),
        utils.common.wrap("🍻 | {0} предложил(а) пива {1} {2}"),
        utils.common.wrap("🍻 | {0} предложил пива {1} {2}"),
        utils.common.wrap("🍻 | {0} предложила пива {1} {2}"),
        form="datv"
    ),
    RP2Handler(
        utils.regex.command("дефенестрировать"),
        utils.rand.rand_or_null_fun("🏠 | {0} отправил(а) в свободное падение {1} {2}", 1, 2, "🪟 | {0} измучил(а) виндой {1} {2}"),
        utils.rand.rand_or_null_fun("🏠 | {0} отправил в свободное падение {1} {2}", 1, 2, "🪟 | {0} измучил виндой {1} {2}"),
        utils.rand.rand_or_null_fun("🏠 | {0} отправила в свободное падение {1} {2}", 1, 2, "🪟 | {0} измучила виндой {1} {2}")
    ),
]


# mention:
#  OR:
#    @(username)
#      where username is (a-zA-Z0-9_){5,64} and can't start with digit
#                        -> using simple check (word-like character)
#    {(uid)|(len)}(name)
#      where uid  is number
#            len  is number
#            name is string of len=len
mention_pattern = utils.regex.ignore_case(
    utils.regex.unite(
        '@' + utils.regex.named('username', r'\w+'),
        r'\{' + utils.regex.named_int('uid') + r'\|' + utils.regex.named_int('len') + r'\}'
    )
)


async def on_rp(cm: utils.cm.CommandMessage):
    user = (await cm.sender.get_mention()).replace('_', '\\_')
    pronoun_set = cm.sender.get_pronouns()
    mention = (await cm.reply_sender.get_mention()).replace('_', '\\_') if cm.reply_sender is not None else None
    res = []
    for line in cm.arg.split('\n')[:20]:  # technical limitation TODO fix!
        # try match to RP-1 as "RP-1 arg"
        for handler in rp1handlers:
            match = re.search(handler.pattern, line)
            if match:
                arg = line[len(match[0]):]
                res.append(handler.invoke(user, pronoun_set, arg))
        # try match to RP-2 as "RP-2 [mention] arg"
        for handler in rp2handlers:
            match = re.search(handler.pattern, line)
            if match:
                arg = line[len(match[0]):]
                cur_mention = mention
                match = re.search(mention_pattern, arg)
                if match:
                    # if matched 'username' then get name
                    # if matched 'uid + len' then get name from text
                    vars = match.groupdict()
                    if vars['username'] is not None:
                        username, arg = match[0][1:], arg[len(match[0]):]
                        cur_user = await utils.user.from_telethon(username, chat=cm.sender.chat_id, client=cm.client)
                        cur_mention = await cur_user.get_mention()
                    else:
                        uid = int(vars['uid'])
                        l = int(vars['len'])
                        arg = arg[len(match[0]):]
                        name, arg = arg[:l], arg[l:]
                        cur_mention = f"[{name}](tg://user?id={uid})"

                if cur_mention is not None or arg is not None:
                    res.append(handler.invoke(user, pronoun_set, (cur_mention or '').replace('_', '\\_') or '', arg))
                else:
                    res.append("RP-2 commands can't be executed without second user mention")
    if res:
        await cm.int_cur.reply('\n'.join(res))


handlers = [utils.ch.CommandHandler("role", re.compile(""), ["role", "рп"], on_rp)]