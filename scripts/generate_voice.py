import os
import wave
import time

from google import genai
from google.genai import types, errors


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing!")


with open("horror_story.txt", "r", encoding="utf-8") as file:
    story = file.read().strip()


if not story:
    raise ValueError("horror_story.txt is empty!")


client = genai.Client(api_key=api_key)


MAX_ATTEMPTS = 6


for attempt in range(1, MAX_ATTEMPTS + 1):

    try:

        print(
            f"🎙️ Generating horror voice... "
            f"attempt {attempt}/{MAX_ATTEMPTS}"
        )

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

                    if (
                        part.inline_data
                        and part.inline_data.data
                    ):
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


        print("✅ AI Horror Voice generated successfully!")
        print("🔊 File created: narration.wav")

        break


    except errors.ClientError as e:

        if attempt == MAX_ATTEMPTS:

            print("❌ Gemini quota error after all attempts.")
            raise


        wait_time = attempt * 30

        print(f"⚠️ Gemini client/quota error: {e}")
        print(f"⏳ Waiting {wait_time} seconds before retry...")

        time.sleep(wait_time)


    except errors.ServerError as e:

        if attempt == MAX_ATTEMPTS:

            print("❌ Gemini server error after all attempts.")
            raise


        wait_time = attempt * 20

        print(f"⚠️ Gemini server busy: {e}")
        print(f"⏳ Waiting {wait_time} seconds before retry...")

        time.sleep(wait_time)


    except Exception as e:

        if attempt == MAX_ATTEMPTS:
            raise

        wait_time = 15

        print(f"⚠️ Voice generation failed: {e}")
        print(f"⏳ Waiting {wait_time} seconds before retry...")

        time.sleep(wait_time)