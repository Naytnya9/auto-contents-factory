import os
import json
import base64
import time

from google import genai


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

    print(f"🎨 Generating Scene {scene_number}...")

    # Retry up to 3 times if Gemini temporarily returns 503
    for attempt in range(3):

        try:

            interaction = client.interactions.create(
                model="gemini-3.1-flash-image",
                input=prompt,
                response_format={
                    "type": "image",
                    "aspect_ratio": "9:16",
                    "image_size": "1K"
                }
            )

            break

        except Exception as e:

            print(
                f"⚠️ Scene {scene_number} "
                f"attempt {attempt + 1} failed: {e}"
            )

            if attempt == 2:
                raise

            print("⏳ Waiting 20 seconds before retry...")
            time.sleep(20)


    image_data = interaction.output_image.data

    image_bytes = base64.b64decode(image_data)

    filename = f"images/scene_{scene_number}.png"

    with open(filename, "wb") as image_file:
        image_file.write(image_bytes)

    print(f"✅ Created: {filename}")


print("👻 All horror images generated successfully!")