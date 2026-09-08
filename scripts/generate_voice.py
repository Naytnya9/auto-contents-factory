import os
import wave

from google import genai
from google.genai import types


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing!")


with open("horror_story.txt", "r", encoding="utf-8") as file:
    story = file.read()


client = genai.Client(api_key=api_key)


response = client.models.generate_content(
    model="gemini-3.1-flash-tts-preview",
    contents=f"""
Read the following Burmese horror story exactly as written.

Use a slow, mysterious and scary storytelling style.
Make the narration dramatic and suspenseful.

Story:

{story}
""",
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Kore"
                )
            )
        )
    )
)


audio_data = response.candidates[0].content.parts[0].inline_data.data


with wave.open("narration.wav", "wb") as audio_file:
    audio_file.setnchannels(1)
    audio_file.setsampwidth(2)
    audio_file.setframerate(24000)
    audio_file.writeframes(audio_data)


print("🎙️ AI Horror Voice generated successfully!")
print("🔊 File created: narration.wav")