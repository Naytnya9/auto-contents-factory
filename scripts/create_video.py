import os
import glob
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont


AUDIO = "narration.wav"
SUBTITLES = "subtitles.json"
OUTPUT = "horror_video.mp4"

FONT_PATH = "/usr/share/fonts/truetype/padauk/Padauk-Regular.ttf"


if not os.path.exists(AUDIO):
    raise FileNotFoundError("narration.wav not found!")

if not os.path.exists(SUBTITLES):
    raise FileNotFoundError("subtitles.json not found!")

if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(
        f"Myanmar font not found: {FONT_PATH}"
    )


images = sorted(
    glob.glob("images/scene_*.png"),
    key=lambda x: int(
        os.path.basename(x).split("_")[1].split(".")[0]
    )
)


if not images:
    raise FileNotFoundError("No scene images found!")


print(f"🎬 Found {len(images)} scene images")


with open(SUBTITLES, "r", encoding="utf-8") as file:
    subtitles = json.load(file)


os.makedirs("subtitle_images", exist_ok=True)


print("📝 Creating Burmese subtitle images...")


font = ImageFont.truetype(
    FONT_PATH,
    52
)


for index, subtitle in enumerate(subtitles):

    text = subtitle["text"]

    canvas = Image.new(
        "RGBA",
        (1080, 250),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(canvas)

    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (1080 - text_width) // 2
    y = (250 - text_height) // 2

    draw.text(
        (x, y),
        text,
        font=font,
        fill="white",
        stroke_width=3,
        stroke_fill="black"
    )

    filename = (
        f"subtitle_images/"
        f"subtitle_{index:03d}.png"
    )

    canvas.save(filename)

    print(f"✅ Created {filename}")


result = subprocess.run(
    [
        "ffprobe",
        "-v", "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        AUDIO
    ],
    capture_output=True,
    text=True,
    check=True
)


duration = float(result.stdout.strip())


image_duration = duration / len(images)


concat_file = "images.txt"


with open(
    concat_file,
    "w",
    encoding="utf-8"
) as file:

    for image in images:

        absolute_path = os.path.abspath(image)

        file.write(
            f"file '{absolute_path}'\n"
        )

        file.write(
            f"duration {image_duration}\n"
        )

    file.write(
        f"file '{os.path.abspath(images[-1])}'\n"
    )


print("🎬 Creating base horror video...")


subprocess.run(
    [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-i", AUDIO,
        "-vf",
        "scale=1080:1920:"
        "force_original_aspect_ratio=increase,"
        "crop=1080:1920",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "23",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-shortest",
        "base_video.mp4"
    ],
    check=True
)


print("🎥 Base video created!")


print("⚠️ Subtitle overlay will be added next.")
print("✅ Base horror video created successfully!")