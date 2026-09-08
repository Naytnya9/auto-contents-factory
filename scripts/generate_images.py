import os
import json
import time

from google import genai
from google.genai import types


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing!")


client = genai.Client(api_key=api_key)


with open("scenes.json", "r", encoding="utf-8") as file:
    data = json.load(file)


os.makedirs("images", exist_ok=True)


for scene in data["scenes"]:

    scene_number = scene["scene_number"]
    prompt = scene["visual_prompt"]

    filename = f"images/scene_{scene_number}.png"

    # Skip if image already exists
    if os.path.exists(filename):
        print(f"⏭️ Scene {scene_number} already exists. Skipping.")
        continue

    print(f"🎨 Generating Scene {scene_number}...")

    response = None

    for attempt in range(5):

        try:

            response = client.models.generate_content(
                model="gemini-3.1-flash-image",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    response_format={
                        "image": {
                            "aspect_ratio": "9:16",
                            "image_size": "1K"
                        }
                    }
                )
            )

            break

        except Exception as e:

            print(
                f"⚠️ Scene {scene_number} "
                f"attempt {attempt + 1}/5 failed:"
            )

            print(e)

            if attempt == 4:
                raise

            wait_time = 30 * (attempt + 1)

            print(
                f"⏳ Waiting {wait_time} seconds "
                f"before retry..."
            )

            time.sleep(wait_time)


    image_saved = False

    for part in response.parts:

        if part.inline_data is not None:

            image = part.as_image()

            image.save(filename)

            image_saved = True

            print(f"✅ Created: {filename}")

            break


    if not image_saved:
        raise RuntimeError(
            f"Gemini returned no image for Scene {scene_number}"
        )


print("👻 All horror images generated successfully!")