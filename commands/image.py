import util

import re
import typing
import io
import PIL.Image
import PIL.ImageFilter


class ImageHandler(typing.NamedTuple):
    pattern: re.Pattern
    handler_impl: typing.Callable[[PIL.Image.Image, str], typing.Awaitable[PIL.Image.Image]]

    async def invoke(self, img: PIL.Image.Image, arg: str = ''):
        return await self.handler_impl(img, arg)


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


async def image_contrast(im: PIL.Image.Image, _: str) -> PIL.Image.Image:
    def find_a_b(arr):
        n, sm, frac = len(arr), sum(arr), 20
        sum1, a = arr[0], 0
        while sum1 * frac < sm:
            sum1, a = sum1 + arr[a + 1], a + 1
        sum2, b = arr[-1], n - 1
        while sum2 * frac < sm:
            sum2, b = sum2 + arr[b - 1], b - 1
        return a, b

    ans = PIL.Image.new("RGB", im.size, "black")
    pix = im.load()
    pix_ans = ans.load()
    for i in range(3):
        c = [0] * 256
        for row in range(im.height):
            for col in range(im.width):
                c[pix[col, row][i]] += 1
        a, b = find_a_b(c)

        for row in range(im.height):
            for col in range(im.width):
                c = list(pix_ans[col, row])
                c[i] = (pix[col, row][i] - a) * 255 // (b - a)
                pix_ans[col, row] = tuple(c)
    return ans


image_handlers = [
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('copy', 'вновь'))),
                 util.to_async(lambda im, _: im)),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('grey', 'серым'))),
                 util.to_async(lambda im, _: im.convert("L"))),
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
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('contrast', 'контраст'))),
                 image_contrast),
    ImageHandler(util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('median', 'медиана'))),
                 util.to_async(lambda im, _: im.filter(PIL.ImageFilter.MedianFilter()))),
]


async def on_image(cm: util.CommandMessage):
    img = PIL.Image.open(await cm.media.get())
    for line in cm.arg.split('\n'):
        for handler in image_handlers:
            match = re.search(handler.pattern, line)
            if match:
                arg = line[len(match[0]):]
                img = await handler.invoke(img, arg)
    file = io.BytesIO()
    img.save(file, "png")
    file.seek(0)
    await cm.int_cur.reply('', file)


handlers = [util.CommandHandler(
    name="image",
    pattern=util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('img', 'pic', 'пикч'))),
    help_message="Image processing",
    author="@yuki_the_girl",
    handler_impl=on_image,
    is_prefix=True,
    required_media_type={'photo'}
)]