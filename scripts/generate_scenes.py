import os
import json
import time

from google import genai
from google.genai import errors


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing!")


with open("horror_story.txt", "r", encoding="utf-8") as file:
    story = file.read().strip()


if not story:
    raise ValueError("horror_story.txt is empty!")


client = genai.Client(api_key=api_key)


prompt = f"""
You are a professional horror movie director and storyboard artist.

Analyze the Burmese horror story below and divide it into
5 to 8 cinematic scenes.

IMPORTANT:
The same characters must look consistent across ALL scenes.

First identify the main characters and define their appearance.
Then use the SAME character descriptions in every relevant scene.

For each scene create:

1. scene_number
2. narration
3. visual_prompt

Each visual_prompt MUST include:

- Character identity
- Character appearance
- Clothing
- Age
- Hair
- Facial features
- Location
- Action
- Camera angle
- Lighting
- Mood
- Cinematic composition
- Vertical 9:16 format

CHARACTER CONSISTENCY RULES:

- Do not change a character's age.
- Do not change their gender.
- Do not change their hairstyle.
- Do not change their clothing unless the story explicitly requires it.
- Do not create a different face for the same character.
- If a character appears again, repeat the same physical description.
- Keep the same environment visually consistent when scenes happen in the same location.

VISUAL STYLE:

- Photorealistic cinematic horror movie
- Realistic human anatomy
- Realistic skin texture
- Natural facial proportions
- Dramatic cinematic lighting
- Dark atmospheric horror mood
- High detail
- Vertical 9:16 composition
- Suitable for TikTok and YouTube Shorts
- No text
- No subtitles
- No logos
- No watermark

IMPORTANT:
The visual_prompt must describe ONLY what should be visible in the image.
Do not describe narration or dialogue inside the image.

Return ONLY valid JSON.

Use exactly this format:

{{
  "characters": [
    {{
      "name": "Character name",
      "description": "Detailed consistent physical appearance and clothing"
    }}
  ],
  "scenes": [
    {{
      "scene_number": 1,
      "narration": "Burmese narration for this scene",
      "visual_prompt": "Detailed English cinematic image prompt"
    }}
  ]
}}

Horror Story:

{story}
"""


MAX_ATTEMPTS = 6


for attempt in range(1, MAX_ATTEMPTS + 1):

    try:

        print(
            f"🎬 Generating cinematic scenes... "
            f"attempt {attempt}/{MAX_ATTEMPTS}"
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        text = response.text.strip()


        # Remove markdown code fences
        if text.startswith("```"):

            lines = text.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            text = "\n".join(lines).strip()


        # Parse JSON
        scenes = json.loads(text)


        # Validate characters
        if "characters" not in scenes:
            raise ValueError(
                "Gemini response does not contain 'characters'."
            )


        # Validate scenes
        if "scenes" not in scenes:
            raise ValueError(
                "Gemini response does not contain 'scenes'."
            )

        if not scenes["scenes"]:
            raise ValueError(
                "Gemini returned an empty scene list."
            )


        # Save JSON
        with open(
            "scenes.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                scenes,
                file,
                ensure_ascii=False,
                indent=2
            )


        print(
            "✅ Cinematic scenes generated successfully!"
        )


        print("\n👤 CHARACTERS:")

        for character in scenes["characters"]:

            print(f"\n{character['name']}")
            print(character["description"])


        print("\n🎬 SCENES:")

        for scene in scenes["scenes"]:

            print(f"\nScene {scene['scene_number']}")
            print(scene["visual_prompt"])


        break


    # 429 / quota errors
    except errors.ClientError as e:

        if attempt == MAX_ATTEMPTS:

            print(
                "❌ Gemini quota error after all attempts."
            )

            raise


        wait_time = attempt * 45

        print(f"⚠️ Gemini client/quota error: {e}")

        print(
            f"⏳ Waiting {wait_time} seconds "
            "before retry..."
        )

        time.sleep(wait_time)


    # 503 / server busy errors
    except errors.ServerError as e:

        if attempt == MAX_ATTEMPTS:

            print(
                "❌ Gemini server error after all attempts."
            )

            raise


        wait_time = attempt * 30

        print(f"⚠️ Gemini server busy: {e}")

        print(
            f"⏳ Waiting {wait_time} seconds "
            "before retry..."
        )

        time.sleep(wait_time)


    # JSON or other errors
    except Exception as e:

        print(
            f"⚠️ Scene generation failed: {e}"
        )

        if attempt == MAX_ATTEMPTS:

            print(
                f"❌ Scene generation failed after "
                f"{MAX_ATTEMPTS} attempts."
            )

            raise


        wait_time = 20

        print(
            f"⏳ Waiting {wait_time} seconds "
            "before retry..."
        )

        time.sleep(wait_time)