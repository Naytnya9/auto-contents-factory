import os
import re
import wave
import json


AUDIO = "narration.wav"
STORY = "horror_story.txt"
OUTPUT = "subtitles.json"


if not os.path.exists(AUDIO):
    raise FileNotFoundError("narration.wav not found!")

if not os.path.exists(STORY):
    raise FileNotFoundError("horror_story.txt not found!")


with open(STORY, "r", encoding="utf-8") as file:
    story = file.read().strip()


if not story:
    raise ValueError("horror_story.txt is empty!")


with wave.open(AUDIO, "rb") as audio:
    frames = audio.getnframes()
    rate = audio.getframerate()
    duration = frames / float(rate)


print(f"🎙️ Audio duration: {duration:.2f} seconds")


story = re.sub(r"\s+", " ", story).strip()


parts = re.split(
    r"(?<=[။!?])\s+",
    story
)


chunks = []

for part in parts:

    part = part.strip()

    if not part:
        continue

    while len(part) > 55:

        split_at = part.rfind(" ", 0, 55)

        if split_at < 20:
            split_at = 55

        chunks.append(part[:split_at].strip())
        part = part[split_at:].strip()

    if part:
        chunks.append(part)


if not chunks:
    raise ValueError("No subtitle text found!")


print(f"📝 Subtitle chunks: {len(chunks)}")


chunk_duration = duration / len(chunks)


subtitles = []


for index, text in enumerate(chunks):

    start = index * chunk_duration
    end = (index + 1) * chunk_duration

    subtitles.append({
        "start": start,
        "end": end,
        "text": text
    })


with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        subtitles,
        file,
        ensure_ascii=False,
        indent=2
    )


print("📝 Subtitle timing created successfully!")
print(f"📄 Output: {OUTPUT}")