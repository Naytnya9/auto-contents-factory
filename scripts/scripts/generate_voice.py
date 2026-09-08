import os
import base64
import wave

from google import genai


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing!")


with open("horror_story.txt", "r", encoding="utf-8") as file:
    story = file.read()


client = genai.Client(api_key=api_key)


prompt = f"""
Read the following Burmese horror story naturally.

Use a slow, mysterious, scary storytelling style.

Add suspense and emotion naturally.

Do not translate or change the words.

Story:

{story}
"""


interaction = client.interactions.create(
    model="gemini-3.1-flash-tts-preview",
    input=prompt,
    response_format={"type": "audio"},
    generation_config={
        "speech_config": [
            {
                "voice": "Kore"
            }
        ]
    }
)


audio_data = base64.b64decode(
    interaction.output_audio.data
)


with wave.open("narration.wav", "wb") as audio_file:
    audio_file.setnchannels(1)
    audio_file.setsampwidth(2)
    audio_file.setframerate(24000)
    audio_file.writeframes(audio_data)


print("🎙️ AI Horror Voice generated successfully!")
print("🔊 File created: narration.wav")