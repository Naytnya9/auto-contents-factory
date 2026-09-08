import os
import time
from google import genai
from google.genai import errors


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing!")


client = genai.Client(api_key=api_key)


prompt = """
You are a professional Burmese horror story writer.

Write one original, cinematic Burmese horror story.

Requirements:

- Write in Burmese language.
- Length: approximately 500 to 700 Burmese words.
- Make it scary, mysterious and cinematic.
- Include a clear beginning, rising tension and frightening ending.
- Use a small number of characters.
- Make the story suitable for a 9:16 TikTok horror video.
- Do not include a title.
- Return only the story text.
"""


MAX_ATTEMPTS = 6


for attempt in range(1, MAX_ATTEMPTS + 1):

    try:

        print(
            f"🤖 Generating horror story... "
            f"Attempt {attempt}/{MAX_ATTEMPTS}"
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        story = response.text.strip()

        if not story:
            raise ValueError("Gemini returned an empty story.")

        with open(
            "horror_story.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(story)

        print("👻 Horror story generated successfully!")
        print(story)

        break


    except errors.ClientError as error:

        if attempt == MAX_ATTEMPTS:
            print("❌ Gemini quota error after all attempts.")
            raise

        wait_time = attempt * 30

        print(f"⚠️ Gemini quota/rate limit reached.")
        print(f"⏳ Waiting {wait_time} seconds...")

        time.sleep(wait_time)


    except errors.ServerError as error:

        if attempt == MAX_ATTEMPTS:
            print("❌ Gemini server error after all attempts.")
            raise

        wait_time = attempt * 20

        print("⚠️ Gemini server is busy.")
        print(f"⏳ Waiting {wait_time} seconds...")

        time.sleep(wait_time)


    except Exception as error:

        print(f"❌ Unexpected error: {error}")

        if attempt == MAX_ATTEMPTS:
            raise

        time.sleep(10)