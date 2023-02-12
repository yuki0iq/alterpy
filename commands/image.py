import util

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


class ImageHandler(typing.NamedTuple):
    pattern: re.Pattern
    handler_impl: typing.Callable[[PIL.Image.Image, str], typing.Awaitable[PIL.Image.Image]]

    async def invoke(self, img: PIL.Image.Image, arg: str = ''):
        return await self.handler_impl(img, arg)


class ImageTwoHandler(typing.NamedTuple):
    pattern: re.Pattern
    handler_impl: typing.Callable[
        [PIL.Image.Image, PIL.Image.Image, str],
        typing.Awaitable[typing.Tuple[PIL.Image.Image, PIL.Image.Image]]
    ]

    async def invoke(self, img: PIL.Image.Image, prev: PIL.Image.Image, arg: str = ''):
        return await self.handler_impl(img, prev, arg)


async def image_scaler(im: PIL.Image.Image, arg: str) -> PIL.Image.Image:
    w, h = im.size
    max_scale_factor = 2560 / max(w, h)
    scale_factor = min(max_scale_factor, util.to_float(arg, 1))
    return im.resize((max(2, int(w * scale_factor)), max(2, int(h * scale_factor))), PIL.Image.LANCZOS)


async def image_brightness_normalizer(im: PIL.Image.Image, _: str) -> PIL.Image.Image:
    im.convert("RGB")
    pix = im.load()
    C = 0
    for row in range(im.height):
        for col in range(im.width):
            C += sum(pix[col, row])
    C = (C / (3 * im.width * im.height)) - 128
    for row in range(im.height):
        for col in range(im.width):
            pix[col, row] = tuple(int(pix[col, row][i] - C) for i in range(3))
    return im


async def image_white_balancer(im: PIL.Image.Image, _: str) -> PIL.Image.Image:
    im.convert("RGB")
    pix = im.load()
    c = [0] * 3
    for row in range(im.height):
        for col in range(im.width):
            for i in range(3):
                c[i] += pix[col, row][i]
    cnt_pix = im.width * im.height
    for i in range(3):
        c[i] = c[i] / cnt_pix
    ca = sum(c) / 3
    for i in range(3):
        c[i] -= ca
    for row in range(im.height):
        for col in range(im.width):
            pix[col, row] = tuple(int(pix[col, row][i] - c[i]) for i in range(3))
    return im


async def image_denoiser(im: PIL.Image.Image, _: str) -> PIL.Image.Image:
    im.convert("RGB")
    ans = im.copy()
    pix = im.load()
    pix_ans = ans.load()
    for row in range(1, im.height - 1):
        for col in range(1, im.width - 1):
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


image_handlers = [
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('copy', 'вновь'))),
                 util.to_async(lambda im, _: im)),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('grey', 'серым'))),
                 util.to_async(lambda im, _: PIL.ImageOps.grayscale(im))),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('spread', 'точками'))),
                 util.to_async(lambda im, arg: im.effect_spread(util.to_int(arg, 10)))),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('blur', 'мыло'))),
                 util.to_async(lambda im, _: im.filter(PIL.ImageFilter.BLUR))),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('contour', 'контур'))),
                 util.to_async(lambda im, _: im.filter(PIL.ImageFilter.CONTOUR))),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('scale', 'масштаб'))),
                 image_scaler),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('left', 'влево'))),
                 util.to_async(lambda im, _: im.transpose(PIL.Image.ROTATE_90))),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('180'))),
                 util.to_async(lambda im, _: im.transpose(PIL.Image.ROTATE_180))),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('right', 'вправо'))),
                 util.to_async(lambda im, _: im.transpose(PIL.Image.ROTATE_270))),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('horiz', 'гориз'))),
                 util.to_async(lambda im, _: im.transpose(PIL.Image.FLIP_LEFT_RIGHT))),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('vert', 'верт'))),
                 util.to_async(lambda im, _: im.transpose(PIL.Image.FLIP_TOP_BOTTOM))),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('bright', 'яркость'))),
                 image_brightness_normalizer),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('white', 'белый'))),
                 image_white_balancer),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('denoise', 'антишум'))),
                 image_denoiser),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('contrast', 'контраст'))),
                 util.to_async(lambda im, _: PIL.ImageOps.autocontrast(im, 5))),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('median', 'медиана'))),
                 util.to_async(lambda im, _: im.filter(PIL.ImageFilter.MedianFilter()))),
    ImageTwoHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('overlay', 'наложить'))),
                    util.to_async(lambda im, pr, _: (im.paste(pr, (0, 0)) or im, pr)))
]


async def on_image(cm: util.CommandMessage):
    img = PIL.Image.open(await cm.media.get())
    prev = PIL.Image.open(await cm.reply_media.get()) if cm.reply_media.type() != "" else None
    text = []
    as_file = False
    for line in cm.arg.split('\n'):
        if line.lower() in ['file', 'файлом']:
            as_file = True
        if line.lower() in ['image', 'картинкой']:
            as_file = False
        if line.lower() in ['swap', 'обменять']:
            img, prev = prev, img
        if line.lower() in ['size', 'размеры']:
            text.append(f"{img.size}")
        for handler in image_handlers:
            match = re.search(handler.pattern, line)
            if match:
                arg = line[len(match[0]):]
                if type(handler) == ImageHandler:
                    img = await handler.invoke(img, arg)
                elif type(handler) == ImageTwoHandler:
                    if prev is None:
                        text.append(f"Can't use two image handler without second image specified, required for command {line}")
                    else:
                        img, prev = await handler.invoke(img, prev, arg)
    text = '\n'.join(text)
    if as_file:
        filename = f"{util.temp_filename()}.png"
        img.save(filename)
        await cm.int_cur.send_file(filename, True, text=text, force_document=True)
    else:
        file = io.BytesIO()
        img.save(file, "png")
        file.seek(0)
        await cm.int_cur.reply(text, file)


handlers = [util.CommandHandler(
    name="image",
    pattern=util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('img', 'pic', 'пикч'))),
    help_message="Image processing",
    handler_impl=on_image,
    is_prefix=True,
    required_media_type={'photo', 'file'}
)]




async def send_image(img: PIL.Image.Image, inter: util.MessageInteractor, text: str):
    file = io.BytesIO()
    img.save(file, "png")
    file.seek(0)
    await inter.reply(text, file)


async def send_image_file(img: PIL.Image.Image, inter: util.MessageInteractor, text: str):
    filename = f"{util.temp_filename()}.png"
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


def re_build(arg: str) -> re.Pattern: return util.re_ignore_case(util.re_pat_starts_with(arg) + '$')
def re_letter() -> str: return '[a-zа-яё]'
def re_space() -> str: return "\\s*"
def re_var() -> str: return re_letter() + util.re_unite(re_letter(), '\\d') + '*'
def re_arg(name: str) -> str: return re_space() + re_named(name, re_var())
def re_num_nat(name: str) -> str: return re_space() + re_named(name, '[1-9]\\d*')
def re_real(name: str) -> str: return re_space() + re_named(name, '\\d*\\.?\\d*')
def re_named(name: str, pat: str) -> str: return f"(?P<{name}>(?!(to|with|в|на|с))({pat}))"
def re_or(*args) -> str: return re_space() + util.re_unite(*args)


class ImageProgrammableHandler(typing.NamedTuple):
    name: str
    pattern: re.Pattern
    help_message: str
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
            + util.re_optional(re_arg('inp'))
        ),
        "help",
        "tasks.append(asyncio.create_task(send_image({inp}, cm.int_cur, '{inp} on line {line}')))"
    ),
    ImageProgrammableHandler(
        'file',
        re_build(
            re_or('файлом', 'file')
            + util.re_optional(re_arg('inp'))
        ),
        "help",
        "tasks.append(asyncio.create_task(send_image_file({inp}, cm.int_cur, '{inp} on line {line}')))"
    ),
    ImageProgrammableHandler(
        'copy',
        re_build(
            re_or('скопировать', 'copy')
            + util.re_optional(re_arg('inp'))
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = {inp}.copy()"
    ),
    ImageProgrammableHandler(
        'swap',
        re_build(
            re_or('обменять', 'swap')
            + util.re_optional(re_arg('inp'))
            + util.re_optional(re_or('с', 'with') + re_arg('sec'))
        ),
        "help",
        "{inp}, {sec} = {sec}, {inp}"
    ),
    ImageProgrammableHandler(
        'gray',
        re_build(
            re_or('серым', 'grey', 'gray')
            + util.re_optional(re_arg('inp'))
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = PIL.ImageOps.grayscale({inp})"
    ),
    ImageProgrammableHandler(
        'spread',
        re_build(
            re_or('точками', 'spread')
            + util.re_optional(re_arg('inp'))
            + util.re_optional(re_num_nat("dist"))
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = {inp}.effect_spread({dist} or 20)"
    ),
    ImageProgrammableHandler(
        'blur',
        re_build(
            re_or('размылить', 'blur')
            + util.re_optional(re_arg('inp'))
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = {inp}.filter(PIL.ImageFilter.BLUR)"
    ),
    ImageProgrammableHandler(
        'contour',
        re_build(
            re_or('контур', 'contour')
            + util.re_optional(re_arg('inp'))
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = {inp}.filter(PIL.ImageFilter.CONTOUR)"
    ),
    ImageProgrammableHandler(
        'scale-inc',
        re_build(
            re_or('масштаб', 'увеличить', 'scale', 'increase')
            + util.re_optional(re_arg('inp'))
            + util.re_unite(
                re_or('в') + re_real('scale_ru') + re_or('раз', 'раза'),
                re_real('scale_en') + re_or('fold')
            )
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = image_scale({inp}, {scale_ru} or {scale_en})"
    ),
    ImageProgrammableHandler(
        'scale-dec',
        re_build(
            re_or('уменьшить', 'decrease')
            + util.re_optional(re_arg('inp'))
            + util.re_unite(
                re_or('в') + re_real('scale_ru') + re_or('раз', 'раза'),
                re_real('scale_en') + re_or('fold')
            )
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = image_scale({inp}, 1 / ({scale_ru} or {scale_en}))"
    ),
    ImageProgrammableHandler(
        'rot-ccw',
        re_build(
            re_or(
                util.re_optional('повернуть') + re_or('влево', 'налево', 'против часовой'),
                util.re_optional('rotate') + re_or('left', 'ccw', 'counterclockwise'),
            )
            + util.re_optional(re_arg('inp'))
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = {inp}.transpose(PIL.Image.ROTATE_90)"
    ),
    ImageProgrammableHandler(
        'rot-cw',
        re_build(
            re_or(
                util.re_optional('повернуть') + re_or('вправо', 'направо', 'по часовой'),
                util.re_optional('rotate') + re_or('right', 'cw', 'clockwise'),
            )
            + util.re_optional(re_arg('inp'))
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = {inp}.transpose(PIL.Image.ROTATE_270)"
    ),
    ImageProgrammableHandler(
        'upside',
        re_build(
            re_or(
                'перевернуть',
                'upside down'
            )
            + util.re_optional(re_arg('inp'))
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = {inp}.transpose(PIL.Image.ROTATE_180)"
    ),
    ImageProgrammableHandler(
        'flip-v',
        re_build(
            re_or('отзеркалить', 'mirror', 'flip')
            + util.re_optional(re_arg('inp'))
            + re_or('по вер', 'по вертикали', 'вертикально', 'vert', 'vertically')
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = {inp}.transpose(PIL.Image.FLIP_TOP_BOTTOM)"
    ),
    ImageProgrammableHandler(
        'flip-h',
        re_build(
            re_or('отзеркалить', 'mirror', 'flip')
            + util.re_optional(re_arg('inp'))
            + re_or('по гор', 'по горизонтали', 'горизонтально', 'hor', 'horiz', 'horizontally')
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = {inp}.transpose(PIL.Image.FLIP_LEFT_RIGHT)"
    ),
    ImageProgrammableHandler(
        'bright',
        re_build(
            re_or('автояркость', 'bright')
            + util.re_optional(re_arg('inp'))
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = image_brightness({inp})"
    ),
    ImageProgrammableHandler(
        'awb',
        re_build(
            re_or('автобаланс', 'awb')
            + util.re_optional(re_arg('inp'))
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = image_white_balance({inp})"
    ),
    ImageProgrammableHandler(
        'denoise',
        re_build(
            re_or('антишум', 'denoise')
            + util.re_optional(re_arg('inp'))
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = image_denoise({inp})"
    ),
    ImageProgrammableHandler(
        'autocontrast',
        re_build(
            re_or('автоконтраст', 'autocontrast')
            + util.re_optional(re_arg('inp'))
            + util.re_optional(re_or('в', 'to') + re_arg('out'))
        ),
        "help",
        "{out} = PIL.ImageOps.autocontrast({inp}, 5)"
    )
]


async def on_image_prog(cm: util.CommandMessage):
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


handlers.append(util.CommandHandler(
    name="image-prog",
    pattern=util.re_ignore_case(util.re_pat_starts_with(util.re_only_prefix() + util.re_unite('pie', 'пирог'))),
    help_message="Programmable image edit",
    handler_impl=on_image_prog,
    is_prefix=True,
    required_media_type={'photo', 'file'}
))

handlers.append(util.CommandHandler(
    name="help-pie",
    pattern=util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite("piehelp", "состав пирога"))),
    help_message="Show help for PIE command",
    handler_impl=util.help_handler([], image_prog_handlers),  # TODO add help
    is_prefix=True
))

