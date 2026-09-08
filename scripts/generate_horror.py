import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing!")

client = genai.Client(api_key=api_key)

prompt = """
Create ONE original short horror story in natural Burmese language.

Requirements:
- The story must be completely original.
- Make it scary, mysterious, and suitable for TikTok.
- Start with a powerful hook.
- Keep the audience curious.
- Include suspense and a surprising twist.
- Use natural Burmese that sounds good for AI voice narration.
- Length: approximately 60 to 90 seconds when narrated.
- Do not use headings.
- Do not explain anything outside the story.

Return only the final Burmese horror narration.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

story = response.text

with open("horror_story.txt", "w", encoding="utf-8") as file:
    file.write(story)

print("👻 AI Horror Story generated successfully!")
print(story)
