import os
import re
import subprocess


SRT_FILE = "subtitles.srt"
OUTPUT_DIR = "subtitle_images"

WIDTH = 1080
HEIGHT = 260


if not os.path.exists(SRT_FILE):
    raise FileNotFoundError("subtitles.srt not found!")


os.makedirs(OUTPUT_DIR, exist_ok=True)


def parse_time(time_text):

    hours, minutes, seconds = re.split(
        r"[:,]",
        time_text
    )

    return (
        int(hours) * 3600
        + int(minutes) * 60
        + int(seconds)
        + int(seconds) * 0
    )


with open(
    SRT_FILE,
    "r",
    encoding="utf-8"
) as file:

    content = file.read().strip()


blocks = re.split(
    r"\n\s*\n",
    content
)


subtitles = []


for block in blocks:

    lines = block.strip().splitlines()

    if len(lines) < 3:
        continue

    index = lines[0]

    text = " ".join(
        lines[2:]
    )

    filename = os.path.join(
        OUTPUT_DIR,
        f"subtitle_{int(index):03d}.png"
    )


    escaped_text = (
        text
        .replace("\\", "\\\\")
        .replace('"', '\\"')
    )


    svg = f"""
<svg width="{WIDTH}" height="{HEIGHT}"
xmlns="http://www.w3.org/2000/svg">

<text
x="50%"
y="50%"
text-anchor="middle"
dominant-baseline="middle"
font-family="Padauk"
font-size="52"
font-weight="bold"
fill="white"
stroke="black"
stroke-width="3"
paint-order="stroke">

{escaped_text}

</text>

</svg>
"""


    svg_file = filename.replace(
        ".png",
        ".svg"
    )


    with open(
        svg_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(svg)


    subprocess.run(
        [
            "rsvg-convert",
            svg_file,
            "-o",
            filename
        ],
        check=True
    )


    subtitles.append(
        {
            "index": int(index),
            "image": filename
        }
    )


print(
    f"✅ Created {len(subtitles)} "
    f"Burmese subtitle images!"
)