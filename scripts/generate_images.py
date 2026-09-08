import os
import json
import requests
import time


api_key = os.environ.get("POLLINATIONS_API_KEY")

if not api_key:
    raise ValueError("POLLINATIONS_API_KEY is missing!")


with open("scenes.json", "r", encoding="utf-8") as file:
    data = json.load(file)


os.makedirs("images", exist_ok=True)


# Build a consistent character reference
character_reference = ""

for character in data.get("characters", []):

    character_reference += (
        f"\nCharacter: {character['name']}\n"
        f"Appearance: {character['description']}\n"
    )


for scene in data["scenes"]:

    scene_number = scene["scene_number"]
    scene_prompt = scene["visual_prompt"]

    filename = f"images/scene_{scene_number}.png"

    print(
        f"🎨 Generating Scene {scene_number}..."
    )

    # Add character consistency information
    final_prompt = f"""
Create a cinematic photorealistic horror movie scene.

CHARACTER CONSISTENCY:
{character_reference}

SCENE:
{scene_prompt}

IMPORTANT:
- Keep every character's face, age, hairstyle and clothing consistent.
- If a character appears in this scene, use the exact same appearance
  described in the character reference.
- Do not invent a different character.
- Keep the same environment consistent when applicable.
- Realistic human anatomy.
- Realistic facial proportions.
- Realistic skin texture.
- Cinematic horror lighting.
- Dark mysterious atmosphere.
- High detail.
- Vertical 9:16 composition.
- No text.
- No subtitles.
- No logo.
- No watermark.
"""

    url = (
        "https://gen.pollinations.ai/image/"
        + requests.utils.quote(final_prompt)
    )

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    params = {
        "model": "flux",
        "width": 576,
        "height": 1024
    }


    # Retry image generation
    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        try:

            print(
                f"🖼️ Image attempt "
                f"{attempt}/{max_attempts}"
            )

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=180
            )

            response.raise_for_status()

            # Make sure the response contains data
            if not response.content:
                raise RuntimeError(
                    "Image API returned empty data."
                )

            with open(
                filename,
                "wb"
            ) as image_file:

                image_file.write(
                    response.content
                )

            print(
                f"✅ Created: {filename}"
            )

            break


        except Exception as e:

            print(
                f"⚠️ Image generation failed: {e}"
            )

            if attempt == max_attempts:
                raise

            wait_time = attempt * 20

            print(
                f"⏳ Waiting {wait_time} seconds..."
            )

            time.sleep(wait_time)


print(
    "👻 All consistent horror images "
    "generated successfully!"
)