#!/usr/bin/python
# vim: encoding=utf-8
# pylint: disable=wrong-import-position,wrong-import-order,redefined-builtin

"""
This module is used to generate png-files for wttr.in queries.
The only exported function is:

* render_ansi(png_file, text, options=None)

`render_ansi` is the main function of the module,
which does rendering of stream into a PNG-file.

The module uses PIL for graphical tasks, and pyte for rendering
of ANSI stream into terminal representation.
"""

from __future__ import print_function

import sys
import io
import os
import glob

from PIL import Image, ImageFont, ImageDraw
import pyte.screens
import emoji
import grapheme

from . import unicodedata2

sys.path.insert(0, "..")

COLS = 180
ROWS = 100
CHAR_WIDTH = 8
CHAR_HEIGHT = 16
FONT_SIZE = 16
FONT_CAT = {
    'default':      "/usr/share/fonts/TTF/FantasqueSansMono-Regular.ttf",
    'Cyrillic':     "/usr/share/fonts/TTF/FantasqueSansMono-Regular.ttf",
    'Greek':        "/usr/share/fonts/TTF/FantasqueSansMono-Regular.ttf",
    'Arabic':       "/usr/share/fonts/Unifont/Unifont_jp.otf",
    'Hebrew':       "/usr/share/fonts/Unifont/Unifont_jp.otf",
    'Han':          "/usr/share/fonts/Unifont/Unifont_jp.otf",
    'Hiragana':     "/usr/share/fonts/Unifont/Unifont_jp.otf",
    'Katakana':     "/usr/share/fonts/Unifont/Unifont_jp.otf",
    'Hangul':       "/usr/share/fonts/Unifont/Unifont_jp.otf",
    'Braille':      "/usr/share/fonts/Unifont/Unifont_jp.otf",
    'Emoji':        "/usr/share/fonts/Unifont/Unifont_jp.otf",
    # Why not "/usr/share/fonts/twemoji/twemoji.ttf"? Because fuck you, pillow
}

WEATHER_SYMBOL_WIDTH_VTE = {
    "✨": 2,
    "☁️": 1,
    "🌫": 2,
    "🌧": 2,
    "🌧": 2,
    "❄️": 1,
    "❄️": 1,
    "🌦": 1,
    "🌦": 1,
    "🌧": 1,
    "🌧": 1,
    "🌨": 2,
    "🌨": 2,
    "⛅️": 2,
    "☀️": 1,
    "🌩": 2,
    "⛈": 1,
    "⛈": 1,
    "☁️": 1,
}

#
# How to find font for non-standard scripts:
#
#   $ fc-list :lang=ja
#
# GNU/Debian packages, that the fonts come from:
#
#   * fonts-dejavu-core
#   * fonts-wqy-zenhei (Han)
#   * fonts-motoya-l-cedar (Hiragana/Katakana)
#   * fonts-lexi-gulim (Hangul)
#   * fonts-symbola (Braille/Emoji)
#


def render_ansi(text, options=None):
    """Render `text` (terminal sequence) in a PNG file
    paying attention to passed command line `options`.

    Return: file content
    """

    screen = pyte.screens.Screen(COLS, ROWS)
    screen.set_mode(pyte.modes.LNM)
    stream = pyte.Stream(screen)

    text, graphemes = _fix_graphemes(text)
    stream.feed(text)

    buf = sorted(screen.buffer.items(), key=lambda x: x[0])
    buf = [[x[1] for x in sorted(line[1].items(), key=lambda x: x[0])] for line in buf]

    return _gen_term(buf, graphemes, options=options)


def _color_mapping(color, inverse=False):
    """Convert pyte color to PIL color

    Return: tuple of color values (R,G,B)
    """

    if color == 'default':
        if inverse:
            return 'black'
        return 'lightgray'

    if color in ['green', 'black', 'cyan', 'blue', 'brown']:
        return color
    try:
        return (
            int(color[0:2], 16),
            int(color[2:4], 16),
            int(color[4:6], 16))
    except (ValueError, IndexError):
        # if we do not know this color and it can not be decoded as RGB,
        # print it and return it as it is (will be displayed as black)
        # print color
        return color
    return color


def _strip_buf(buf):
    """Strips empty spaces from behind and from the right side.
    (from the right side is not yet implemented)
    """

    def empty_line(line):
        "Returns True if the line consists from spaces"
        return all(x.data == ' ' for x in line)

    def line_len(line):
        "Returns len of the line excluding spaces from the right"

        last_pos = len(line)
        while last_pos > 0 and line[last_pos-1].data == ' ':
            last_pos -= 1
        return last_pos

    number_of_lines = 0
    for line in buf[::-1]:
        if not empty_line(line):
            break
        number_of_lines += 1

    if number_of_lines:
        buf = buf[:-number_of_lines]

    max_len = max(line_len(x) for x in buf)
    buf = [line[:max_len] for line in buf]

    return buf


def _script_category(char):
    """Returns category of a Unicode character

    Possible values:
        default, Cyrillic, Greek, Han, Hiragana
    """

    if emoji.is_emoji(char):
        return "Emoji"

    cat = unicodedata2.script_cat(char)[0]
    if char == u'：':
        return 'Han'
    if cat in ['Latin', 'Common']:
        return 'default'
    return cat


def _load_emojilib():
    """Load known emojis from a directory, and return dictionary
    of PIL Image objects correspodent to the loaded emojis.
    Each emoji is resized to the CHAR_HEIGHT size.
    """

    emojilib = {}
    for filename in glob.glob("share/emoji/*.png"):
        character = os.path.basename(filename)[:-3]
        emojilib[character] = \
            Image.open(filename).resize((CHAR_HEIGHT, CHAR_HEIGHT))
    return emojilib

# pylint: disable=too-many-locals,too-many-branches,too-many-statements


def _gen_term(buf, graphemes, options=None):
    """Renders rendered pyte buffer `buf` and list of workaround `graphemes`
    to a PNG file, and return its content
    """

    if not options:
        options = {}

    current_grapheme = 0

    buf = _strip_buf(buf)
    cols = max(len(x) for x in buf)
    rows = len(buf)

    bg_color = 0
    if "background" in options:
        bg_color = _color_mapping(options["background"], options.get("inverted_colors"))

    image = Image.new('RGB', (cols * CHAR_WIDTH, rows * CHAR_HEIGHT), color=bg_color)

    buf = buf[-ROWS:]

    draw = ImageDraw.Draw(image)
    font = {}
    for cat in FONT_CAT:
        font[cat] = ImageFont.truetype(FONT_CAT[cat], FONT_SIZE)

    emojilib = _load_emojilib()

    x_pos = 0
    y_pos = 0
    for line in buf:
        x_pos = 0
        for char in line:
            current_color = _color_mapping(char.fg, options.get("inverted_colors"))
            if char.bg != 'default':
                draw.rectangle(
                    ((x_pos, y_pos),
                     (x_pos+CHAR_WIDTH, y_pos+CHAR_HEIGHT)),
                    fill=_color_mapping(char.bg, options.get("inverted_colors")))

            if char.data == "!":
                try:
                    data = graphemes[current_grapheme]
                except IndexError:
                    pass
                current_grapheme += 1
            else:
                data = char.data

            if data:
                cat = _script_category(data[0])
                if cat not in font:
                    print("Unknown font category: %s" % cat)
                if cat == 'Emoji' and emojilib.get(data):
                    image.paste(emojilib.get(data), (x_pos, y_pos))
                else:
                    draw.text(
                        (x_pos, y_pos),
                        data,
                        font=font.get(cat, font.get('default')),
                        fill=current_color)

            x_pos += CHAR_WIDTH * WEATHER_SYMBOL_WIDTH_VTE.get(data, 1)
        y_pos += CHAR_HEIGHT

    if 'transparency' in options:
        transparency = options.get('transparency', '255')
        try:
            transparency = int(transparency)
        except ValueError:
            transparency = 255

        if transparency < 0:
            transparency = 0

        if transparency > 255:
            transparency = 255

        image = image.convert("RGBA")
        datas = image.getdata()

        new_data = []
        for item in datas:
            new_item = tuple(list(item[:3]) + [transparency])
            new_data.append(new_item)

        image.putdata(new_data)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format="png")
    return img_bytes.getvalue()


def _fix_graphemes(text):
    """
    Extract long graphemes sequences that can't be handled
    by pyte correctly because of the bug pyte#131.
    Graphemes are omited and replaced with placeholders,
    and returned as a list.

    Return:
        text_without_graphemes, graphemes
    """

    output = ""
    graphemes = []

    for gra in grapheme.graphemes(text):
        if len(gra) > 1:
            character = "!"
            graphemes.append(gra)
        else:
            character = gra
        output += character

    return output, graphemes
