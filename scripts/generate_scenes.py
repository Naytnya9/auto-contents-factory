import os
import json
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


response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

text = response.text.strip()

# Remove markdown code fences if Gemini adds them
if text.startswith("```"):
    text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text[:-3]

scenes = json.loads(text)

with open("scenes.json", "w", encoding="utf-8") as file:
    json.dump(scenes, file, ensure_ascii=False, indent=2)


print("🎬 Horror scenes generated successfully!")

for scene in scenes["scenes"]:
    print(f"\nScene {scene['scene_number']}")
    print(scene["visual_prompt"])