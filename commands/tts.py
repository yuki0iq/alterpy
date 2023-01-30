import util

import gtts
import re


def on_tts_wrapper(lang: str):
    async def on_tts(cm: util.CommandMessage):
        filename = f"{util.temp_filename()}.mp3"
        gtts.gTTS(cm.arg, lang=lang).save(filename)
        await cm.int_cur.send_file(filename, as_reply=True, voice_note=True)
    return on_tts


handlers = [
    util.CommandHandler("tts-en", re.compile(util.re_pat_starts_with("/?(say|tts)")), "Say message in English", "@yuki_the_girl", on_tts_wrapper("en"), is_prefix=True),
    util.CommandHandler("tts-ru", re.compile(util.re_pat_starts_with("/?(скажи)")), "Сказать голосом на русском", "@yuki_the_girl", on_tts_wrapper("ru"), is_prefix=True)
]
