import utils.cm
import utils.ch
import utils.regex
import utils.locale

handler_list = []

translations = {
    'size': {
        'en': "Can't parse size",
        'ru': 'Не удалось обнаружить размер',
    },
    'bmi': {
        'en': 'Your BMI is {bmi} ({text})',
        'ru': 'Ваш ИМТ --- {bmi} ({text})',
    },
    'vals': {
        'en': ['underweight', 'normal', 'overweight', 'obesity'],
    },
}

LOC = utils.locale.Localizator(translations)


async def on_bmi(cm: utils.cm.CommandMessage) -> None:
    try:
        h, m = map(float, cm.arg.split())
    except:
        await cm.int_cur.reply(LOC.obj('size', cm.lang))
        return

    _bmi = int((1000000 * m) / (h * h))

    text = LOC.obj('vals', cm.lang)[[_bmi < 1850, _bmi < 2500, _bmi < 3000, True].index(True)]

    bmi = '000' + str(_bmi)
    bmi = bmi[:-2].lstrip('0') + '.' + bmi[-2:]
    if bmi[0] == '.':
        bmi = '0' + bmi

    await cm.int_cur.reply(eval(LOC.get('bmi', cm.lang)))


handler_list.append(utils.ch.CommandHandler(
    name="bmi",
    pattern=utils.regex.cmd(utils.regex.unite('bmi', 'имт')),
    help_page="bmi",
    handler_impl=on_bmi,
    is_prefix=True
))
