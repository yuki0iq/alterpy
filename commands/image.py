import utils.interactor
import utils.file
import utils.cm
import utils.ch
import utils.regex
import utils.help

import asyncio
import traceback
import re
import typing
import io
import PIL.Image
import PIL.ImageFilter
import PIL.ImageChops
import PIL.ImageMath
import PIL.ImageOps
import PIL.ImageStat


async def send_image(img: PIL.Image.Image, inter: utils.interactor.MessageInteractor, text: str):
    file = io.BytesIO()
    img.save(file, "png")
    file.seek(0)
    await inter.reply(text, file)


async def send_image_file(img: PIL.Image.Image, inter: utils.interactor.MessageInteractor, text: str):
    filename = f"{utils.file.temp_filename()}.png"
    img.save(filename)
    await inter.send_file(filename, True, caption=text, force_document=True)


def image_scale(img: PIL.Image.Image, scale: float) -> PIL.Image.Image:
    w, h = img.size
    max_scale_factor = 2560 / max(w, h)
    scale_factor = min(max_scale_factor, scale)
    return img.resize((max(2, int(w * scale_factor)), max(2, int(h * scale_factor))), PIL.Image.LANCZOS)


def image_brightness(img: PIL.Image.Image) -> PIL.Image.Image:
    img = img.convert("RGB")
    return PIL.Image.merge("RGB", tuple(
        PIL.ImageMath.eval('band - C + 128',
                           band=band,
                           C=int(round(sum(PIL.ImageStat.Stat(img).mean) / 3))).convert('L')
        for band in img.split()
    ))


def image_white_balance(img: PIL.Image.Image) -> PIL.Image.Image:
    img = img.convert("RGB")
    C = int(round(sum(PIL.ImageStat.Stat(img).mean) / 3))
    return PIL.Image.merge("RGB", tuple(
        PIL.ImageMath.eval('band - Cb + C',
                           band=band,
                           Cb=int(round(PIL.ImageStat.Stat(band).mean[0])),
                           C=C).convert('L')
        for band in img.split()
    ))


def image_denoise(img: PIL.Image.Image) -> PIL.Image.Image:
    # TODO: rewrite
    img = img.convert("RGB")
    ans = img.copy()
    pix = img.load()
    pix_ans = ans.load()
    for row in range(1, img.height - 1):
        for col in range(1, img.width - 1):
            a = [[] for i in range(3)]
            for i in range(3):
                for d_row in [-1, 0, 1]:
                    for d_col in [-1, 0, 1]:
                        a[i].append(pix[col + d_col, row + d_row][i])
            a = list(map(sorted, a))
            c = list(pix[col, row])
            for i in range(3):
                if c[i] == a[i][0]:
                    c[i] = a[i][1]
                if c[i] == a[i][8]:
                    c[i] = a[i][7]
            pix_ans[col, row] = tuple(c)
    return ans


def re_build(arg: str) -> re.Pattern: return utils.regex.raw_command(arg + '$')
def re_letter() -> str: return '[a-zа-яё]'
def re_space() -> str: return "\\s*"
def re_var() -> str: return re_letter() + utils.regex.unite(re_letter(), '\\d') + '*'
def re_arg(name: str) -> str: return re_space() + re_named(name, re_var())
def re_num_nat(name: str) -> str: return re_space() + re_named(name, '[1-9]\\d*')
def re_real(name: str) -> str: return re_space() + re_named(name, '\\d*\\.?\\d*')
def re_named(name: str, pat: str) -> str: return f"(?P<{name}>(?!((to|with|в|на|с)\\b))({pat}))"
def re_or(*args) -> str: return re_space() + utils.regex.unite(*args)


class ImageProgrammableHandler(typing.NamedTuple):
    name: str
    pattern: re.Pattern
    help_message: str
    help_message_en: str
    help_message_ru: str
    handler_impl: str

    def apply(self, line: str) -> str | None:
        replace_variables = {
            'соо': 'msg',
            'ответ': 'rep'
        }

        line = re.sub('\\s+', ' ', line.lower())
        mat = re.search(self.pattern, line)
        if mat:
            code = self.handler_impl
            vars = mat.groupdict()
            if not vars.get('inp', ''): vars['inp'] = 'msg'
            if not vars.get('sec', ''): vars['sec'] = 'rep'
            if not vars.get('out', ''): vars['out'] = vars['inp']
            for name, var in vars.items():
                code = code.replace("{" + name + "}", str(replace_variables.get(var, var)))
            return code


#приклеить КАРТИНКУ снизу/сверху/слева/справа к ДРУГОЙ (в ТРЕТЬЮ)
#уравнять ширину/высоту КАРТИНКУ в соотв(етствие) с ДРУГОЙ (в ТРЕТЬЮ)

image_prog_handlers = [
    ImageProgrammableHandler(
        'send',
        re_build(
            re_or('картинкой', 'отправить', 'image', 'send')
            + utils.regex.optional(re_arg('inp'))
        ),
        "",
        "help-en",
        "help-ru",
        "tasks.append(asyncio.create_task(send_image({inp}, cm.int_cur, '{inp} on line {line}')))"
    ),
    ImageProgrammableHandler(
        'file',
        re_build(
            re_or('файлом', 'file')
            + utils.regex.optional(re_arg('inp'))
        ),
        "",
        "help-en",
        "help-ru",
        "tasks.append(asyncio.create_task(send_image_file({inp}, cm.int_cur, '{inp} on line {line}')))"
    ),
    ImageProgrammableHandler(
        'copy',
        re_build(
            re_or('скопировать', 'copy')
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = {inp}.copy()"
    ),
    ImageProgrammableHandler(
        'swap',
        re_build(
            re_or('обменять', 'swap')
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.optional(re_or('с', 'with') + re_arg('sec'))
        ),
        "",
        "help-en",
        "help-ru",
        "{inp}, {sec} = {sec}, {inp}"
    ),
    ImageProgrammableHandler(
        'gray',
        re_build(
            re_or('серым', 'grey', 'gray')
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = PIL.ImageOps.grayscale({inp})"
    ),
    ImageProgrammableHandler(
        'spread',
        re_build(
            re_or('точками', 'spread')
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.optional(re_num_nat("dist"))
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = {inp}.effect_spread({dist} or 20)"
    ),
    ImageProgrammableHandler(
        'blur',
        re_build(
            re_or('размылить', 'blur')
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = {inp}.filter(PIL.ImageFilter.BLUR)"
    ),
    ImageProgrammableHandler(
        'contour',
        re_build(
            re_or('контур', 'contour')
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = {inp}.filter(PIL.ImageFilter.CONTOUR)"
    ),
    ImageProgrammableHandler(
        'scale-inc',
        re_build(
            re_or('масштаб', 'увеличить', 'scale', 'increase')
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.unite(
                re_or('в') + re_real('scale_ru') + re_or('раз', 'раза'),
                re_real('scale_en') + re_or('fold')
            )
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = image_scale({inp}, {scale_ru} or {scale_en})"
    ),
    ImageProgrammableHandler(
        'scale-dec',
        re_build(
            re_or('уменьшить', 'decrease')
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.unite(
                re_or('в') + re_real('scale_ru') + re_or('раз', 'раза'),
                re_real('scale_en') + re_or('fold')
            )
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = image_scale({inp}, 1 / ({scale_ru} or {scale_en}))"
    ),
    ImageProgrammableHandler(
        'rot-ccw',
        re_build(
            re_or(
                utils.regex.optional('повернуть') + re_or('влево', 'налево', 'против часовой'),
                utils.regex.optional('rotate') + re_or('left', 'ccw', 'counterclockwise'),
            )
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = {inp}.transpose(PIL.Image.ROTATE_90)"
    ),
    ImageProgrammableHandler(
        'rot-cw',
        re_build(
            re_or(
                utils.regex.optional('повернуть') + re_or('вправо', 'направо', 'по часовой'),
                utils.regex.optional('rotate') + re_or('right', 'cw', 'clockwise'),
            )
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = {inp}.transpose(PIL.Image.ROTATE_270)"
    ),
    ImageProgrammableHandler(
        'upside',
        re_build(
            re_or(
                'перевернуть',
                'upside down'
            )
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = {inp}.transpose(PIL.Image.ROTATE_180)"
    ),
    ImageProgrammableHandler(
        'flip-v',
        re_build(
            re_or('отзеркалить', 'mirror', 'flip')
            + utils.regex.optional(re_arg('inp'))
            + re_or('по вер', 'по вертикали', 'вертикально', 'vert', 'vertically')
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = {inp}.transpose(PIL.Image.FLIP_TOP_BOTTOM)"
    ),
    ImageProgrammableHandler(
        'flip-h',
        re_build(
            re_or('отзеркалить', 'mirror', 'flip')
            + utils.regex.optional(re_arg('inp'))
            + re_or('по гор', 'по горизонтали', 'горизонтально', 'hor', 'horiz', 'horizontally')
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = {inp}.transpose(PIL.Image.FLIP_LEFT_RIGHT)"
    ),
    ImageProgrammableHandler(
        'bright',
        re_build(
            re_or('автояркость', 'bright')
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = image_brightness({inp})"
    ),
    ImageProgrammableHandler(
        'awb',
        re_build(
            re_or('автобаланс', 'awb')
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = image_white_balance({inp})"
    ),
    ImageProgrammableHandler(
        'denoise',
        re_build(
            re_or('антишум', 'denoise')
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = image_denoise({inp})"
    ),
    ImageProgrammableHandler(
        'autocontrast',
        re_build(
            re_or('автоконтраст', 'autocontrast')
            + utils.regex.optional(re_arg('inp'))
            + utils.regex.optional(re_or('в', 'to') + re_arg('out'))
        ),
        "",
        "help-en",
        "help-ru",
        "{out} = PIL.ImageOps.autocontrast({inp}, 5)"
    )
]


async def on_image_prog(cm: utils.cm.CommandMessage):
    if not cm.arg:
        await cm.int_cur.reply("Can't PIE with empty code!")
        return

    msg = PIL.Image.open(await cm.media.get())
    rep = PIL.Image.open(await cm.reply_media.get()) if cm.reply_media.type() != "" else None

    image_code = []
    text = []
    lines = cm.arg.split('\n')
    for line, idx in zip(lines, range(1,1+len(lines))):
        if not line:
            continue
        code_line = None
        for handler in image_prog_handlers:
            code_line = handler.apply(line)
            if code_line:
                break
        if code_line is None:
            text.append(f"`{line}` is not recognised as an image command")
        else:
            image_code.append(code_line.replace('{line}', str(idx)))
    if text:
        text = '\n'.join(text)
        await cm.int_cur.reply(f"Parse error(s) occurred:\n{text}")
        return

    image_code = '\n'.join(image_code)
    code = f"tasks = []\n{image_code}"
    code_locals = dict()
    try:
        exec(code, globals() | locals(), code_locals)
        if code_locals['tasks']:
            await asyncio.wait(code_locals['tasks'])
    except:
        code_lines = code.split('\n')
        lined_code = '\n'.join(f"{i}  {code_lines[i]}" for i in range(len(code_lines)))
        await cm.int_cur.reply(f"```{traceback.format_exc()}```\nWhile executing following code:\n```{lined_code}```")


handlers = [utils.ch.CommandHandler(
    name="image-prog",
    pattern=utils.regex.pre_command(utils.regex.unite('pie', 'пирог')),
    help_page=["pie", "пирог"],
    handler_impl=on_image_prog,
    is_prefix=True,
    required_media_type={'photo', 'file'}
)]

utils.help.add(handlers, "PIE", "piehelp", "pie", is_eng=True)
utils.help.add(handlers, "PIE", "состав пирога", "pie", is_eng=False)

