import utils.ch
import utils.cm
import utils.regex
import utils.rand
import utils.common
import utils.locale
import utils.user
import utils.str
import utils.pronouns
import typing
import re


def inflect_mention(mention: str, form: str, lang: str = "ru") -> str:
    if not mention:
        return mention
    le, ri = 1, mention.rindex(']')
    lt = utils.locale.lang(lang)
    return mention[:le] + lt.inflect(lt.tr(mention[le:ri]), form) + mention[ri:]


def inflect_mentions(mentions: [str], form: str, lang: str = "ru") -> str:
    if not mentions:
        return ""
    lt = utils.locale.lang(lang)
    return lt.ander(inflect_mention(mention, form, lang) for mention in mentions)


class RP1Handler(typing.NamedTuple):
    pattern: re.Pattern
    ans: list[typing.Callable[[], str]]

    def invoke(self, user, pronouns, comment):
        return self.ans[utils.pronouns.to_int(pronouns)]().format(user, comment).strip()


class RP2Handler(typing.NamedTuple):
    pattern: re.Pattern
    ans: list[typing.Callable[[], str]]
    lang: str = "ru"
    form: str = "accs"

    def invoke(self, user, pronouns, mention, comment):
        return self.ans[utils.pronouns.to_int(pronouns)]().format(
            user, inflect_mentions(list(m[1] for m in mention), self.form, self.lang), comment
        ).strip().replace('  ', ' ', 1)


rp1handlers = [
    RP1Handler(
        utils.regex.command("задолбало"),
        [
            utils.rand.rand_or_null_fun("😭 | {0} успешно выпилился(ась) {1}", 1, 6, "🎉 | {0} не смог(ла) выпилиться {1}"),
            utils.rand.rand_or_null_fun("😭 | {0} успешно выпилился {1}", 1, 6, "🎉 | {0} не смог выпилиться {1}"),
            utils.rand.rand_or_null_fun("😭 | {0} успешно выпилилась {1}", 1, 6, "🎉 | {0} не смогла выпилиться {1}"),
            utils.rand.rand_or_null_fun("😭 | {0} успешно выпилилось {1}", 1, 6, "🎉 | {0} не смогло выпилиться {1}"),
            utils.rand.rand_or_null_fun("😭 | {0} успешно выпилилось {1}", 1, 6, "🎉 | {0} не смогло выпилиться {1}"),
            utils.rand.rand_or_null_fun("😭 | {0} успешно выпилились {1}", 1, 6, "🎉 | {0} не смогли выпилиться {1}"),
        ]
    )
]

rp2handlers = [
    RP2Handler(
        utils.regex.command("обнять"),
        [
            utils.common.wrap("🤗 | {0} обнял(а) {1} {2}"),
            utils.common.wrap("🤗 | {0} обнял {1} {2}"),
            utils.common.wrap("🤗 | {0} обняла {1} {2}"),
            utils.common.wrap("🤗 | {0} обняло {1} {2}"),
            utils.common.wrap("🤗 | {0} обняло {1} {2}"),
            utils.common.wrap("🤗 | {0} обняли {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("дать"),
        [
            utils.common.wrap("🎁 | {0} дал(а) {1} {2}"),
            utils.common.wrap("🎁 | {0} дал {1} {2}"),
            utils.common.wrap("🎁 | {0} дала {1} {2}"),
            utils.common.wrap("🎁 | {0} дало {1} {2}"),
            utils.common.wrap("🎁 | {0} дало {1} {2}"),
            utils.common.wrap("🎁 | {0} дали {1} {2}"),
        ],
        form="datv",
    ),
    RP2Handler(
        utils.regex.command("сломать"),
        [
            utils.common.wrap("🔧 | {0} сломал(а) {1} {2}"),
            utils.common.wrap("🔧 | {0} сломал {1} {2}"),
            utils.common.wrap("🔧 | {0} сломала {1} {2}"),
            utils.common.wrap("🔧 | {0} сломало {1} {2}"),
            utils.common.wrap("🔧 | {0} сломало {1} {2}"),
            utils.common.wrap("🔧 | {0} сломали {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("убить"),
        [
            utils.common.wrap("☠ | {0} убил(а) {1} {2}"),
            utils.common.wrap("☠ | {0} убил {1} {2}"),
            utils.common.wrap("☠ | {0} убила {1} {2}"),
            utils.common.wrap("☠ | {0} убило {1} {2}"),
            utils.common.wrap("☠ | {0} убило {1} {2}"),
            utils.common.wrap("☠ | {0} убили {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("расстрелять"),
        [
            utils.common.wrap("🔫 | {0} расстрелял(а) {1} {2}"),
            utils.common.wrap("🔫 | {0} расстрелял {1} {2}"),
            utils.common.wrap("🔫 | {0} расстреляла {1} {2}"),
            utils.common.wrap("🔫 | {0} расстреляло {1} {2}"),
            utils.common.wrap("🔫 | {0} расстреляло {1} {2}"),
            utils.common.wrap("🔫 | {0} расстреляли {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("поцеловать"),
        [
            utils.common.wrap("😘 | {0} поцеловал(а) {1} {2}"),
            utils.common.wrap("😘 | {0} поцеловал {1} {2}"),
            utils.common.wrap("😘 | {0} поцеловала {1} {2}"),
            utils.common.wrap("😘 | {0} поцеловало {1} {2}"),
            utils.common.wrap("😘 | {0} поцеловало {1} {2}"),
            utils.common.wrap("😘 | {0} поцеловали {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("кусь(нуть){0,1}|укусить"),
        [
            utils.common.wrap("😬 | {0} кусьнул(а) {1} {2}"),
            utils.common.wrap("😬 | {0} кусьнул {1} {2}"),
            utils.common.wrap("😬 | {0} кусьнула {1} {2}"),
            utils.common.wrap("😬 | {0} кусьнуло {1} {2}"),
            utils.common.wrap("😬 | {0} кусьнуло {1} {2}"),
            utils.common.wrap("😬 | {0} кусьнули {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("пнуть"),
        [
            utils.common.wrap("👞 | {0} пнул(а) {1} {2}"),
            utils.common.wrap("👞 | {0} пнул {1} {2}"),
            utils.common.wrap("👞 | {0} пнула {1} {2}"),
            utils.common.wrap("👞 | {0} пнуло {1} {2}"),
            utils.common.wrap("👞 | {0} пнуло {1} {2}"),
            utils.common.wrap("👞 | {0} пнули {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("прижать"),
        [
            utils.common.wrap("🤲 | {0} прижал(а) {1} {2}"),
            utils.common.wrap("🤲 | {0} прижал {1} {2}"),
            utils.common.wrap("🤲 | {0} прижала {1} {2}"),
            utils.common.wrap("🤲 | {0} прижало {1} {2}"),
            utils.common.wrap("🤲 | {0} прижало {1} {2}"),
            utils.common.wrap("🤲 | {0} прижали {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("погладить"),
        [
            utils.common.wrap("🤲 | {0} погладил(а) {1} {2}"),
            utils.common.wrap("🤲 | {0} погладил {1} {2}"),
            utils.common.wrap("🤲 | {0} погладила {1} {2}"),
            utils.common.wrap("🤲 | {0} погладило {1} {2}"),
            utils.common.wrap("🤲 | {0} погладило {1} {2}"),
            utils.common.wrap("🤲 | {0} погладили {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("потрогать"),
        [
            utils.common.wrap("🙌 | {0} потрогал(а) {1} {2}"),
            utils.common.wrap("🙌 | {0} потрогал {1} {2}"),
            utils.common.wrap("🙌 | {0} потрогала {1} {2}"),
            utils.common.wrap("🙌 | {0} потрогало {1} {2}"),
            utils.common.wrap("🙌 | {0} потрогало {1} {2}"),
            utils.common.wrap("🙌 | {0} потрогали {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("лизнуть"),
        [
            utils.common.wrap("👅 | {0} лизнул(а) {1} {2}"),
            utils.common.wrap("👅 | {0} лизнул {1} {2}"),
            utils.common.wrap("👅 | {0} лизнула {1} {2}"),
            utils.common.wrap("👅 | {0} лизнуло {1} {2}"),
            utils.common.wrap("👅 | {0} лизнуло {1} {2}"),
            utils.common.wrap("👅 | {0} лизнули {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("понюхать"),
        [
            utils.common.wrap("👃 | {0} понюхал(а) {1} {2}"),
            utils.common.wrap("👃 | {0} понюхал {1} {2}"),
            utils.common.wrap("👃 | {0} понюхала {1} {2}"),
            utils.common.wrap("👃 | {0} понюхало {1} {2}"),
            utils.common.wrap("👃 | {0} понюхало {1} {2}"),
            utils.common.wrap("👃 | {0} понюхали {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("ударить"),
        [
            utils.common.wrap("🤜😵 | {0} ударил(а) {1} {2}"),
            utils.common.wrap("🤜😵 | {0} ударил {1} {2}"),
            utils.common.wrap("🤜😵 | {0} ударила {1} {2}"),
            utils.common.wrap("🤜😵 | {0} ударило {1} {2}"),
            utils.common.wrap("🤜😵 | {0} ударило {1} {2}"),
            utils.common.wrap("🤜😵 | {0} ударили {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("шлепнуть"),
        [
            utils.common.wrap("👏 | {0} шлепнул(а) {1} {2}"),
            utils.common.wrap("👏 | {0} шлепнул {1} {2}"),
            utils.common.wrap("👏 | {0} шлепнула {1} {2}"),
            utils.common.wrap("👏 | {0} шлепнуло {1} {2}"),
            utils.common.wrap("👏 | {0} шлепнуло {1} {2}"),
            utils.common.wrap("👏 | {0} шлепнули {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("шлёпнуть"),
        [
            utils.common.wrap("👏 | {0} шлёпнул(а) {1} {2}"),
            utils.common.wrap("👏 | {0} шлёпнул {1} {2}"),
            utils.common.wrap("👏 | {0} шлёпнула {1} {2}"),
            utils.common.wrap("👏 | {0} шлёпнуло {1} {2}"),
            utils.common.wrap("👏 | {0} шлёпнуло {1} {2}"),
            utils.common.wrap("👏 | {0} шлёпнули {1} {2}"),
        ]
    ),
    RP2Handler(
        utils.regex.command("предложить пива"),
        [
            utils.common.wrap("🍻 | {0} предложил(а) пива {1} {2}"),
            utils.common.wrap("🍻 | {0} предложил пива {1} {2}"),
            utils.common.wrap("🍻 | {0} предложила пива {1} {2}"),
            utils.common.wrap("🍻 | {0} предложило пива {1} {2}"),
            utils.common.wrap("🍻 | {0} предложило пива {1} {2}"),
            utils.common.wrap("🍻 | {0} предложили пива {1} {2}"),
        ],
        form="datv"
    ),
    RP2Handler(
        utils.regex.command("дефенестрировать"),
        [
            utils.rand.rand_or_null_fun("🏠 | {0} отправил(а) в свободное падение {1} {2}", 1, 2, "🪟 | {0} измучил(а) виндой {1} {2}"),
            utils.rand.rand_or_null_fun("🏠 | {0} отправил в свободное падение {1} {2}", 1, 2, "🪟 | {0} измучил виндой {1} {2}"),
            utils.rand.rand_or_null_fun("🏠 | {0} отправила в свободное падение {1} {2}", 1, 2, "🪟 | {0} измучила виндой {1} {2}"),
            utils.rand.rand_or_null_fun("🏠 | {0} отправило в свободное падение {1} {2}", 1, 2, "🪟 | {0} измучило виндой {1} {2}"),
            utils.rand.rand_or_null_fun("🏠 | {0} отправило в свободное падение {1} {2}", 1, 2, "🪟 | {0} измучило виндой {1} {2}"),
            utils.rand.rand_or_null_fun("🏠 | {0} отправили в свободное падение {1} {2}", 1, 2, "🪟 | {0} измучили виндой {1} {2}"),
        ]
    ),
]


async def on_rp(cm: utils.cm.CommandMessage):
    user = await cm.sender.get_mention()
    pronoun_set = cm.sender.get_pronouns()
    default_mention = [(cm.reply_sender, await cm.reply_sender.get_mention())] if cm.reply_sender is not None else []
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
                arg = arg.lstrip()
                match = re.search(utils.user.mention_pattern, arg)
                cur_mention = []
                while match:
                    # if matched 'username' then get name
                    # if matched 'uid + len' then get name from text TODO
                    vars = match.groupdict()
                    if vars['username'] is not None:
                        username, arg = match[0][1:], arg[len(match[0]):]
                        cur_user = await utils.user.from_telethon(username, chat=cm.sender.chat_id, client=cm.client)
                        mention = await cur_user.get_mention()
                    else:
                        uid = int(vars['uid'])
                        l = int(vars['len'])
                        arg = arg[len(match[0]):]
                        name, arg = arg[:l], arg[l:]
                        cur_user = await utils.user.from_telethon(uid, chat=cm.sender.chat_id, client=cm.client)
                        mention = f"[{utils.str.escape(name)}](tg://user?id={uid})"
                    cur_mention.append((cur_user, mention))
                    arg = arg.lstrip()
                    match = re.search(utils.user.mention_pattern, arg)
                cur_mention = cur_mention or default_mention

                if cur_mention or arg:
                    res.append(handler.invoke(user, pronoun_set, cur_mention or '', arg))
                else:
                    res.append("RP-2 commands can't be executed without second user mention")
    if res:
        await cm.int_cur.reply('\n'.join(res), link_preview=False)


handler_list = [utils.ch.CommandHandler("role", re.compile(""), ["role", "рп"], on_rp)]



async def on_role(cm: utils.cm.CommandMessage):
    self_mention = [(cm.sender, await cm.sender.get_mention())]
    pronoun_set = cm.sender.get_pronouns()
    default_mention = [(cm.reply_sender, await cm.reply_sender.get_mention())] if cm.reply_sender is not None else []
    chat_id = cm.sender.chat_id
    client = cm.client
    res = []
    for line in cm.arg.split('\n'):
        if line[0] != '~':
            continue

        line = f"MENTION0 {line[1:]}"
        mentions = self_mention[:]

        pre, user, mention, post = await utils.user.from_str(line, chat_id, client)
        while user:
            line = f"{pre}MENTION{len(mentions)}{post}"
            mentions.append((user, mention))
            pre, user, mention, post = await utils.user.from_str(line, chat_id, client)

        line, need_second_mention = utils.locale.lang('en').to_role(line)  # TODO lang

        if '%' in line and default_mention:
            line = line.replace('%', f'MENTION{len(mentions)}')
            mentions.extend(default_mention)

        if need_second_mention and len(mentions) == 1:
            mentions.extend(default_mention)
            line = f"{line} MENTION1"

        if len(mentions) == 1:
            res.append("newRP-2 commands can't be executed without second user mention")  # TODO lang
        else:
            for i in range(len(mentions) - 1, -1, -1):
                line = line.replace(f'MENTION{i}', mentions[i][1])
            res.append(line)
    if res:
        await cm.int_cur.reply('\n'.join(res), link_preview=False)


handler_list.append(utils.ch.CommandHandler("role-new", utils.regex.ignore_case("(^|\n)~"), ["role", "рп"], on_role))
