import utils

import gtts


def on_tts_wrapper(lang: str):
    async def on_tts(cm: utils.cm.CommandMessage):
        filename = f"{utils.file.temp_filename()}.mp3"
        try:
            if len(cm.arg) > 250:
                await cm.int_cur.reply("Please wait while message is being processed...")
            gtts.gTTS(cm.arg, lang=lang).save(filename)
            await cm.int_cur.send_file(filename, as_reply=True, voice_note=True)
        except:
            await cm.int_cur.reply("Empty messages can't be TTSd")
    return on_tts


def tts_handler(name: str, lang: str) -> utils.ch.CommandHandler:
    return utils.ch.CommandHandler(f"tts-{lang}", utils.regex.command(name), ["tts", "озвучка"], on_tts_wrapper(lang), is_prefix=True)


handlers = [
    tts_handler("tts", "en"),
    tts_handler("озвучь", "ru"),
    tts_handler("мова божія", "uk"),
    tts_handler("vnsay", "jp"),
    tts_handler("sayccp", "zh"),
    tts_handler("kosay", "ko")
]
