import os
import glob
import subprocess


AUDIO = "narration.wav"
OUTPUT = "horror_video.mp4"


if not os.path.exists(AUDIO):
    raise FileNotFoundError("narration.wav not found!")


images = sorted(
    glob.glob("images/scene_*.png"),
    key=lambda x: int(
        os.path.basename(x).split("_")[1].split(".")[0]
    )
)


if not images:
    raise FileNotFoundError("No scene images found!")


print(f"🎬 Found {len(images)} scene images")


# Get narration duration
result = subprocess.run(
    [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        AUDIO
    ],
    capture_output=True,
    text=True,
    check=True
)


duration = float(result.stdout.strip())

print(f"🎙️ Narration duration: {duration:.2f} seconds")


# Give each image equal screen time
image_duration = duration / len(images)

print(
    f"🖼️ Each scene duration: "
    f"{image_duration:.2f} seconds"
)


# Create concat file
concat_file = "images.txt"


with open(concat_file, "w", encoding="utf-8") as file:

    for image in images:

        absolute_path = os.path.abspath(image)

        file.write(
            f"file '{absolute_path}'\n"
        )

        file.write(
            f"duration {image_duration}\n"
        )

    # Repeat final image
    file.write(
        f"file '{os.path.abspath(images[-1])}'\n"
    )


print("🎬 Creating horror video...")


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
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        OUTPUT
    ],
    check=True
)


print("✅ Horror video created successfully!")
print(f"🎥 Output: {OUTPUT}")