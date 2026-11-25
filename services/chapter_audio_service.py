import asyncio
import os
import tempfile

from pydub import AudioSegment

import edge_tts

async def create_sentence_mp3(
    text,
    rate="+0%"
):

    file_path = tempfile.NamedTemporaryFile(
        suffix=".mp3",
        delete=False
    ).name

    communicate = edge_tts.Communicate(
        text=text,
        voice="zh-CN-XiaoxiaoNeural",
        rate=rate
    )

    await communicate.save(file_path)

    return file_path

async def create_chapter_mp3(

    sentences,

    output_name,

    rate="+0%",

    pause_ms=1000

):

    final_audio = AudioSegment.empty()

    silence = AudioSegment.silent(
        duration=pause_ms
    )

    for sentence in sentences:

        temp_mp3 = await create_sentence_mp3(
            sentence,
            rate
        )

        segment = AudioSegment.from_mp3(
            temp_mp3
        )

        final_audio += segment

        final_audio += silence

        try:
            os.remove(temp_mp3)

        except:
            pass

    output_file = os.path.join(

        tempfile.gettempdir(),

        f"{output_name}.mp3"

    )

    final_audio.export(
        output_file,
        format="mp3"
    )

    return output_file
