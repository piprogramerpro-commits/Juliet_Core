import asyncio
import edge_tts
import uuid

VOICE = "es-ES-ElviraNeural"

async def _speak(text, file):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(file)


def speak(text):
    file = f"/tmp/{uuid.uuid4()}.mp3"
    asyncio.run(_speak(text, file))
    return file
