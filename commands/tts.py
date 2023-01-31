import util

import gtts
import re


def on_tts_wrapper(lang: str):
    async def on_tts(cm: util.CommandMessage):
        filename = f"{util.temp_filename()}.mp3"
        try:
            if len(cm.arg) > 250:
                await cm.int_cur.reply("Please wait while message is being processed...")
            gtts.gTTS(cm.arg, lang=lang).save(filename)
            await cm.int_cur.send_file(filename, as_reply=True, voice_note=True)
        except:
            await cm.int_cur.reply("Empty messages can't be TTSd")
    return on_tts


handlers = [
    util.CommandHandler("tts-en", re.compile(util.re_pat_starts_with("/?(say|tts)")),
                        "Say message in English", "@yuki_the_girl", on_tts_wrapper("en"), is_prefix=True),
    util.CommandHandler("tts-ru", re.compile(util.re_pat_starts_with("/?(скажи)")),
                        "Сказать голосом на русском", "@yuki_the_girl", on_tts_wrapper("ru"), is_prefix=True),
    util.CommandHandler("tts-jp", re.compile(util.re_pat_starts_with("/?(vnsay)")),
                        "Say message in Japanese", "@yuki_the_girl", on_tts_wrapper("ja"), is_prefix=True),
    util.CommandHandler("tts-zh", re.compile(util.re_pat_starts_with("/?(sayccp)")),
                        "Say message in Chinese", "@yuki_the_girl", on_tts_wrapper("zh"), is_prefix=True),
    util.CommandHandler("tts-ko", re.compile(util.re_pat_starts_with("/?(kosay)")),
                        "Say message in Korean", "@yuki_the_girl", on_tts_wrapper("ko"), is_prefix=True)
]