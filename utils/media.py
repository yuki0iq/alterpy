import telethon.tl.custom
import typing
import io


class Media(typing.NamedTuple):
    message: telethon.tl.custom.message.Message

    async def get(self) -> io.BytesIO:
        file = io.BytesIO()
        if self.message:
            await self.message.download_media(file)
            file.seek(0)
            return file

    def type(self) -> str:
        if not (self.message and self.message.media): return ""
        if self.message.photo: return "photo"
        if self.message.video: return "video"
        if self.message.video_note: return "round"
        if self.message.audio: return "audio"
        if self.message.voice: return "voice"
        if self.message.gif: return "gif"
        if self.message.file: return "file"
        return "unknown"