import os
import time
import wave
from google import genai
from google.genai import errors


API_KEY = os.environ.get("GEMINI_API_KEY")
STORY_FILE = "horror_story.txt"
OUTPUT_FILE = "narration.wav"

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing!")

if not os.path.exists(STORY_FILE):
    raise FileNotFoundError("horror_story.txt not found!")


with open(STORY_FILE, "r", encoding="utf-8") as file:
    story = file.read().strip()


client = genai.Client(api_key=API_KEY)


prompt = f"""
Read the following Burmese horror story naturally as a dramatic,
slow and scary narration.

Use a mysterious horror storytelling style.

Story:

{story}
"""


MAX_ATTEMPTS = 6


def save_pcm_as_wav(pcm_data, output_file, sample_rate=24000):
    with wave.open(output_file, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm_data)


for attempt in range(1, MAX_ATTEMPTS + 1):

    try:

        print(
            f"🎙️ Generating AI voice... "
            f"Attempt {attempt}/{MAX_ATTEMPTS}"
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
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
                        hasattr(part, "inline_data")
                        and part.inline_data
                        and part.inline_data.data
                    ):
                        audio_data = part.inline_data.data
                        break

                if audio_data:
                    break


        if not audio_data:
            raise ValueError(
                "Gemini did not return audio data."
            )


        save_pcm_as_wav(audio_data, OUTPUT_FILE)

        print("✅ AI voice generated successfully!")
        print(f"🎵 Output: {OUTPUT_FILE}")

        break


    except errors.ClientError:

        if attempt == MAX_ATTEMPTS:
            print("❌ Gemini quota error after all attempts.")
            raise

        wait_time = attempt * 30

        print("⚠️ Gemini quota/rate limit reached.")
        print(f"⏳ Waiting {wait_time} seconds...")

        time.sleep(wait_time)


    except errors.ServerError:

        if attempt == MAX_ATTEMPTS:
            print("❌ Gemini server error after all attempts.")
            raise

        wait_time = attempt * 20

        print("⚠️ Gemini server is busy.")
        print(f"⏳ Waiting {wait_time} seconds...")

        time.sleep(wait_time)


    except Exception as error:

        print(f"❌ Error: {error}")

        if attempt == MAX_ATTEMPTS:
            raise

        time.sleep(10)