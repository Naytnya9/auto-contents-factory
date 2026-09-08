import os
import wave
import time

from google import genai
from google.genai import types


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing!")


with open("horror_story.txt", "r", encoding="utf-8") as file:
    story = file.read()


client = genai.Client(api_key=api_key)


for attempt in range(3):

    try:

        print(f"🎙️ Generating horror voice... attempt {attempt + 1}/3")

        response = client.models.generate_content(
            model="gemini-3.1-flash-tts-preview",
            contents=f"""
Read the following Burmese horror story as a narrator.

Use a slow, mysterious, scary and suspenseful storytelling style.

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

        audio_data = None

        if response.candidates:

            for candidate in response.candidates:

                if not candidate.content:
                    continue

                if not candidate.content.parts:
                    continue

                for part in candidate.content.parts:

                    if part.inline_data and part.inline_data.data:

                        audio_data = part.inline_data.data
                        break

                if audio_data:
                    break


        if not audio_data:
            raise RuntimeError(
                "Gemini returned no audio data."
            )


        with wave.open("narration.wav", "wb") as audio_file:

            audio_file.setnchannels(1)
            audio_file.setsampwidth(2)
            audio_file.setframerate(24000)
            audio_file.writeframes(audio_data)


        print("🎙️ AI Horror Voice generated successfully!")
        print("🔊 File created: narration.wav")

        break


    except Exception as e:

        print(f"⚠️ Voice generation failed: {e}")

        if attempt == 2:
            raise

        print("⏳ Waiting 20 seconds before retry...")
        time.sleep(20)