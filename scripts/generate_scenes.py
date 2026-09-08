import os
import json
import time
from google import genai


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing!")


with open("horror_story.txt", "r", encoding="utf-8") as file:
    story = file.read()


client = genai.Client(api_key=api_key)


prompt = f"""
You are a professional horror video director.

Analyze this Burmese horror story and divide it into
5 to 8 cinematic scenes.

For each scene create:

1. scene_number
2. narration
3. visual_prompt

Rules for visual_prompt:

- Write in English.
- Make it cinematic and photorealistic.
- Describe the location, characters, action, lighting and mood.
- Horror movie atmosphere.
- Vertical 9:16 composition for TikTok.
- Do not include text or subtitles in the image.

Return ONLY valid JSON.

Use exactly this format:

{{
  "scenes": [
    {{
      "scene_number": 1,
      "narration": "Burmese narration for this scene",
      "visual_prompt": "English cinematic horror image prompt"
    }}
  ]
}}

Horror Story:

{story}
"""


# Retry Gemini if the server is temporarily unavailable
max_attempts = 4

for attempt in range(1, max_attempts + 1):

    try:

        print(
            f"🎬 Generating horror scenes... "
            f"attempt {attempt}/{max_attempts}"
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

        # Remove markdown code fences if Gemini adds them
        if text.startswith("```"):

            lines = text.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            text = "\n".join(lines).strip()

        # Convert Gemini response to JSON
        scenes = json.loads(text)

        # Basic validation
        if "scenes" not in scenes:
            raise ValueError(
                "Gemini response does not contain 'scenes'."
            )

        if not scenes["scenes"]:
            raise ValueError(
                "Gemini returned an empty scene list."
            )

        # Save scenes
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
            "🎬 Horror scenes generated successfully!"
        )

        for scene in scenes["scenes"]:

            print(
                f"\nScene {scene['scene_number']}"
            )

            print(
                scene["visual_prompt"]
            )

        # Success — stop retry loop
        break


    except Exception as e:

        print(
            f"⚠️ Scene generation failed: {e}"
        )

        if attempt == max_attempts:

            print(
                "❌ Gemini failed after "
                f"{max_attempts} attempts."
            )

            raise

        wait_time = attempt * 30

        print(
            f"⏳ Waiting {wait_time} seconds "
            "before retry..."
        )

        time.sleep(wait_time)