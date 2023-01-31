import util

import re
import traceback

handlers = []


async def on_exec(cm: util.CommandMessage):
    try:
        shifted_arg = cm.arg.replace('\n', '\n    ')
        code = '\n'.join([
            f"import asyncio",
            f"async def func():",
            f"    {shifted_arg}",
            f"task = asyncio.get_event_loop().create_task(func())",
            f"asyncio.wait(task)"
        ])
        exec(code, globals() | locals())
    except:
        await cm.int_cur.reply(f"```{traceback.format_exc()}```")
        if 'code' in locals():
            code_lines = code.split('\n')
            lined_code = '\n'.join(f"{i+1}  {code_lines[i]}" for i in range(len(code_lines)))
            await cm.int_cur.reply(f"While executing following code:\n```{lined_code}```")


handlers.append(util.CommandHandler(
    "exec",
    re.compile(util.re_pat_starts_with("/?(exec)")),
    "Execute python code",
    "@yuki_the_girl",
    on_exec,
    is_prefix=True,
    is_elevated=True
))
