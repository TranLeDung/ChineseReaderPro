import edge_tts
import tempfile


VOICE = "zh-CN-XiaoxiaoNeural"


async def create_audio(
    text,
    rate="+0%"
):

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".mp3",
        delete=False
    )

    path = temp_file.name

    temp_file.close()

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=rate
    )

    await communicate.save(path)

    return path