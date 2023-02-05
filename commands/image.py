import util

import re
import typing
import io
import PIL.Image
import PIL.ImageFilter
import PIL.ImageChops
import PIL.ImageOps


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
    author="@yuki_the_girl",
    handler_impl=on_image,
    is_prefix=True,
    required_media_type={'photo', 'file'}
)]