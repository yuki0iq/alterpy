import dataclasses
import re
import typing
import utils.aiospeller
import utils.ch
import utils.cm
import utils.common
import utils.locale
import utils.log
import utils.pronouns
import utils.rand
import utils.regex
import utils.str
import utils.user


log = utils.log.get("rp")


def inflect_mention(mention: str, form: str, lt) -> str:
    if not mention:
        return mention
    le, ri = 1, mention.rindex(']')
    inflected = lt.inflect(lt.tr(mention[le:ri]), form)
    assert isinstance(inflected, str)
    return mention[:le] + inflected + mention[ri:]


def inflect_mentions(mentions: list[str], form: str, lt) -> str:
    if not mentions:
        return ""
    anded = lt.ander(inflect_mention(mention, form, lt) for mention in mentions)
    assert isinstance(anded, str)
    return anded


def to_role(words: list[str], p: int) -> str:
    return ''.join(utils.locale.try_verb_past(w, p) for w in words if w)


@dataclasses.dataclass
class RP2Handler:
    pattern: re.Pattern[str]
    verb: typing.Callable[[], str]
    emoji: str
    lang: str = "ru"
    form: str = "accs"

    def __post_init__(self):
        self.lang = utils.locale.lang(self.lang)

    def invoke(self, user: str, pronouns: None | int | list[int], mention: list[tuple[utils.user.User, str]], comment: str) -> str:
        return "{e} | {s} {v} {m} {c}".format(
            e=self.emoji,
            s=user,
            v=to_role(utils.regex.split_by_word_border(self.verb()), utils.pronouns.to_int(pronouns)),
            m=inflect_mentions(list(m[1] for m in mention), self.form, self.lang),
            c=comment,
        ).strip().replace('  ', ' ', 1)


rp2handlers = [
    RP2Handler(utils.regex.cmd("обнять"), utils.common.wrap("обнять"), "🤗"),
    RP2Handler(utils.regex.cmd("выебать"), utils.common.wrap("выебать"), "😈"),
    RP2Handler(utils.regex.cmd("дать"), utils.common.wrap("дать"), "🎁", form="datv"),
    RP2Handler(utils.regex.cmd("сломать"), utils.common.wrap("сломать"), "🔧"),
    RP2Handler(utils.regex.cmd("убить"), utils.common.wrap("убить"), "☠"),
    RP2Handler(utils.regex.cmd("расстрелять"), utils.common.wrap("расстрелять"), "🔫"),
    RP2Handler(utils.regex.cmd("поцеловать"), utils.common.wrap("поцеловать"), "😘"),
    RP2Handler(utils.regex.cmd("кусь(нуть){0,1}|укусить"), utils.common.wrap("кусьнуть"), "😬"),
    RP2Handler(utils.regex.cmd("пнуть"), utils.common.wrap("пнуть"), "👞"),
    RP2Handler(utils.regex.cmd("прижать"), utils.common.wrap("прижать"), "🤲"),
    RP2Handler(utils.regex.cmd("погладить"), utils.common.wrap("погладить"), "🤲"),
    RP2Handler(utils.regex.cmd("потрогать"), utils.common.wrap("потрогать"), "🙌"),
    RP2Handler(utils.regex.cmd("лизнуть"), utils.common.wrap("лизнуть"), "👅"),
    RP2Handler(utils.regex.cmd("понюхать"), utils.common.wrap("понюхать"), "👃"),
    RP2Handler(utils.regex.cmd("ударить"), utils.common.wrap("ударить"), "🤜😵"),
    RP2Handler(utils.regex.cmd("шлепнуть"), utils.common.wrap("шлепнуть"), "👏"),
    RP2Handler(utils.regex.cmd("шлёпнуть"), utils.common.wrap("шлёпнуть"), "👏"),
    RP2Handler(utils.regex.cmd("предложить пива"), utils.common.wrap("предложить пива"), "🍻", form="datv"),
    RP2Handler(utils.regex.cmd("дефенестрировать"), utils.rand.rand_or_null_fun("отправить в свободное падение", 1, 2, "измучить виндой"), "🪟"),
]


async def on_rp(cm: utils.cm.CommandMessage) -> None:
    # cm = cm._replace(arg=await utils.aiospeller.correct(alterpy.context.session, cm.arg))
    user = await cm.sender.get_mention()
    pronoun_set = cm.sender.get_pronouns()
    default_mention = [(cm.reply_sender, await cm.reply_sender.get_mention())] if cm.reply_sender is not None else []
    res = []
    for line in cm.arg.split('\n')[:20]:  # technical limitation TODO fix!
        cur_pronoun_set = utils.pronouns.to_int(pronoun_set)
        # try match to RP-2 as "RP-2 [mention] arg"
        for handler in rp2handlers:
            try:
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
                        res.append(handler.invoke(user, cur_pronoun_set, cur_mention, arg))
            except ValueError:
                res.append("Could not parse mention")
    if res:
        await cm.int_cur.reply('\n'.join(res), link_preview=False)


async def on_role(cm: utils.cm.CommandMessage) -> None:
    self_mention = [(cm.sender, await cm.sender.get_mention())]
    pronoun_set = cm.sender.get_pronouns()
    default_mention = [(cm.reply_sender, await cm.reply_sender.get_mention())] if cm.reply_sender is not None else []
    chat_id = cm.sender.chat_id
    client = cm.client
    res = []
    for line in cm.arg.split('\n'):
        if not line or len(line) < 2 or line[0] != '~' or line[-1] == '~' or line[1].isdigit():
            continue

        line = f"MENTION0 {line[1:]}"
        mentions = self_mention[:]

        pre, user, mention, post = await utils.user.from_str(line, chat_id, client)
        while user:
            line = f"{pre}MENTION{len(mentions)}{post}"
            mentions.append((user, mention))
            pre, user, mention, post = await utils.user.from_str(line, chat_id, client)

        words = utils.regex.split_by_word_border(line)
        line = to_role(words, utils.pronouns.to_int(pronoun_set))  # TODO inflect mentions!!
        need_second_mention = len(words) <= 5

        if '%' in line and default_mention:
            line = line.replace('%', f'MENTION{len(mentions)}')
            mentions.extend(default_mention)

        if need_second_mention and len(mentions) == 1:
            mentions.extend(default_mention)
            line = f"{line} MENTION1"

        if not need_second_mention or len(mentions) != 1:
            for i in range(len(mentions) - 1, -1, -1):
                line = line.replace(f'MENTION{i}', mentions[i][1])
            res.append(line)
    if res:
        await cm.int_cur.reply('\n'.join(res), link_preview=False)


handler_list = [
    utils.ch.CommandHandler("role", re.compile(""), "role", on_rp),
    utils.ch.CommandHandler("role-new", utils.regex.ignore_case("(^|\n)~.*(?<!~)($|\n)"), "role", on_role),
]

