import os
import re
import wave


AUDIO = "narration.wav"
STORY = "horror_story.txt"
OUTPUT = "subtitles.srt"


if not os.path.exists(AUDIO):
    raise FileNotFoundError("narration.wav not found!")

if not os.path.exists(STORY):
    raise FileNotFoundError("horror_story.txt not found!")


# Read Burmese story
with open(STORY, "r", encoding="utf-8") as file:
    story = file.read().strip()


if not story:
    raise ValueError("horror_story.txt is empty!")


# Get audio duration
with wave.open(AUDIO, "rb") as audio:
    frames = audio.getnframes()
    rate = audio.getframerate()
    duration = frames / float(rate)


print(f"🎙️ Audio duration: {duration:.2f} seconds")


# Clean text
story = re.sub(r"\s+", " ", story).strip()


# Split into short subtitle chunks
# Burmese does not always use spaces between words,
# so split mainly by punctuation and character length.
parts = re.split(
    r"(?<=[။!?])\s+",
    story
)


chunks = []

for part in parts:

    part = part.strip()

    if not part:
        continue

    # Keep subtitles readable
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


# Divide audio time across subtitle chunks
chunk_duration = duration / len(chunks)


def format_time(seconds):

    hours = int(seconds // 3600)

    minutes = int(
        (seconds % 3600) // 60
    )

    secs = int(seconds % 60)

    milliseconds = int(
        round((seconds - int(seconds)) * 1000)
    )

    if milliseconds >= 1000:

        milliseconds = 0
        secs += 1

    if secs >= 60:

        secs = 0
        minutes += 1

    if minutes >= 60:

        minutes = 0
        hours += 1

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{secs:02d},"
        f"{milliseconds:03d}"
    )


# Create SRT
with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as file:

    for index, text in enumerate(chunks, start=1):

        start = (index - 1) * chunk_duration
        end = index * chunk_duration

        file.write(
            f"{index}\n"
        )

        file.write(
            f"{format_time(start)} --> "
            f"{format_time(end)}\n"
        )

        file.write(
            f"{text}\n\n"
        )


print("📝 Burmese subtitles created successfully!")
print(f"📄 Output: {OUTPUT}")