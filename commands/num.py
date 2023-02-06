import util

handlers = []


async def on_bmi(cm: util.CommandMessage):
    try:
        h, m = map(int, cm.arg.split())
    except:
        await cm.int_cur.reply("Can't parse size")
        return

    bmi = (1000000 * m) // (h * h)

    text = ["underweight", "normal", "overweight", "obesity"][[bmi < 1850, bmi < 2500, bmi < 3000, True].index(True)]

    bmi = '000' + str(bmi)
    bmi = bmi[:-2].lstrip('0') + '.' + bmi[-2:]
    if bmi[0] == '.':
        bmi = '0' + bmi

    await cm.int_cur.reply(f"Your BMI is {bmi} ({text})")


handlers.append(util.CommandHandler(
    name="bmi",
    pattern=util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('bmi', 'имт'))),
    help_message="height (cm) weight (kg) -> BMI (body mass index)",
    author="@yuki_the_girl",
    handler_impl=on_bmi,
    is_prefix=True
))