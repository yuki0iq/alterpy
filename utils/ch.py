import utils.cm
import utils.log
import utils.regex
import utils.media

import typing
import re
import traceback
import inspect


class CommandHandler(typing.NamedTuple):
    name: str  # command name
    pattern: re.Pattern[str]  # regex pattern
    help_page: str
    handler_impl: typing.Callable[[utils.cm.CommandMessage], typing.Awaitable[None]]
    is_prefix: bool = False  # should a command be deleted from its message when passed to handler
    is_elevated: bool = False  # should a command be invoked only if user is admin
    is_arg_current: bool = False  # don't take arg from reply if set
    required_media_type: typing.Set[str] = set()

    async def invoke(self, cm: utils.cm.CommandMessage) -> None:
        if not self.is_elevated or cm.sender.is_admin():
            try:
                await self.handler_impl(cm)
            except:
                await cm.int_cur.reply(f"Exception occurred.\n```{traceback.format_exc()}```")
                utils.log.get("handler").exception("invoke exception")
        else:
            await cm.int_cur.reply("Only bot admins can run elevated commands")


def apply(cm: utils.cm.CommandMessage, ch: CommandHandler) -> utils.cm.CommandMessage:
    arg = re.sub(ch.pattern, '', cm.arg)
    if not len(arg) and not ch.is_arg_current:
        arg = cm.rep
    if not cm.msg.media and not ch.is_arg_current:
        cm = cm._replace(media=cm.reply_media)
    return cm._replace(arg=arg)


def simple_reply(
        msg: str,
        ans: typing.Union[str, typing.Callable[[], typing.Union[typing.Awaitable[str], str]]],
        help_page: str = "",
        pattern: typing.Union[str, re.Pattern[str]] = ""
) -> CommandHandler:
    """
    Simple reply handler. [In]msg -> [Out]ans

    ans: str -- simple replier
    ans: Callable[[], maybe Awaitable str] -- call before reply

    pattern: str OR re.Pattern[str]
    """

    if isinstance(ans, str):
        async def on_simple_reply_str(cm: utils.cm.CommandMessage) -> None:
            await cm.int_cur.reply(ans)

        on_simple_reply = on_simple_reply_str
    elif inspect.iscoroutinefunction(ans):
        async def on_simple_reply_async(cm: utils.cm.CommandMessage) -> None:
            ret = await ans()
            if ret:
                await cm.int_cur.reply(ret)

        on_simple_reply = on_simple_reply_async
    else:
        async def on_simple_reply_fun(cm: utils.cm.CommandMessage) -> None:
            ret = ans()
            if ret:
                await cm.int_cur.reply(ret)

        on_simple_reply = on_simple_reply_fun

    if not pattern:
        pattern = utils.regex.pat_starts_with(msg)
    if isinstance(pattern, str):
        pattern = utils.regex.ignore_case(pattern)

    return CommandHandler(
        name=msg,
        pattern=pattern,
        help_page=help_page,
        handler_impl=on_simple_reply,
        is_prefix=False,
        is_elevated=False
    )
