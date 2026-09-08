import os
import json
import requests


api_key = os.environ.get("POLLINATIONS_API_KEY")

if not api_key:
    raise ValueError("POLLINATIONS_API_KEY is missing!")


with open("scenes.json", "r", encoding="utf-8") as file:
    data = json.load(file)


os.makedirs("images", exist_ok=True)


for scene in data["scenes"]:

    scene_number = scene["scene_number"]
    prompt = scene["visual_prompt"]

    filename = f"images/scene_{scene_number}.png"

    print(f"🎨 Generating Scene {scene_number}...")

    url = "https://gen.pollinations.ai/image/" + requests.utils.quote(prompt)

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    params = {
        "model": "flux",
        "width": 576,
        "height": 1024
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=180
    )

    response.raise_for_status()

    with open(filename, "wb") as image_file:
        image_file.write(response.content)

    print(f"✅ Created: {filename}")


print("👻 All horror images generated successfully!")