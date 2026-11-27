"""Export review clips and a transparent counter for the Final Cut handoff."""

import argparse
import csv
import os
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = (
    ("01_intro_transitions", 27.40, 55.20, "인사, 5만 원 문답, 장갑 구간의 연결과 발화 확인"),
    ("02_bite1_setup", 182.80, 192.60, "접어서 먹어도 되는지 묻는 대화부터 첫 입까지"),
    ("03_bite1_reaction", 196.80, 205.60, "맛있는데요, 평소에 고등어 좋아하세요, 제일 좋아해요"),
    ("04_bite2_setup", 238.20, 246.10, "잠시만요부터 두 번째 입과 첫 반응까지"),
    ("05_bite2_dialogue_rice", 251.70, 265.50, "가시와 살에 대한 문답에서 밥 요청으로 연결"),
    ("06_brand_bite5_bridge", 334.25, 345.65, "브랜드 이름 반응에서 마지막 입으로 넘어가는 연결"),
    ("07_success_dialogue", 391.70, 400.90, "성공 축하부터 상금 안내와 장갑을 빼도 되는지 묻는 대화"),
    ("08_reward_goodbye", 409.80, 425.50, "상금 수령과 인사, 촬영 말미 대화 후보"),
)
FISH = (
    (0, 2), (2, 2), (2, 1), (4, 1), (4, 0), (7, 0), (7, 1),
    (9, 1), (9, 2), (10, 2), (10, 1), (12, 1), (12, 5),
    (10, 5), (10, 4), (9, 4), (9, 5), (7, 5), (7, 6),
    (4, 6), (4, 5), (2, 5), (2, 4), (0, 4),
)


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-n", *map(str, args)], check=True)


def draw_counter(folder, font_path):
    width, height = 880, 196
    mint = (176, 244, 196)
    gold = (255, 221, 131)
    title = ImageFont.truetype(str(font_path), 37)
    label = ImageFont.truetype(str(font_path), 34)
    for count in range(6):
        image = Image.new("RGBA", (width, height))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((1, 1, width - 2, height - 2), 24,
                               fill=(13, 29, 25, 237), outline=(104, 168, 134, 240), width=2)
        draw.text((35, 30), "FISH QUEST", fill=mint, font=title, anchor="lt")
        draw.text((width - 35, 31), f"{count} / 5", fill=gold, font=label, anchor="rt")
        tile_width, gap = 149, 16
        for index in range(5):
            x = (width - 5 * tile_width - 4 * gap) // 2 + index * (tile_width + gap)
            active = index < count
            draw.rounded_rectangle((x, 86, x + tile_width, 162), 11,
                                   fill=(38, 79, 57) if active else (26, 43, 38),
                                   outline=(134, 206, 160) if active else (72, 99, 86), width=2)
            left = x + (tile_width - 60) // 2
            draw.polygon([(left + px * 5, 109 + py * 5) for px, py in FISH],
                         fill=mint if active else (110, 132, 121))
            draw.rectangle((left + 10, 119, left + 14, 123), fill=(13, 29, 25))
        image.save(folder / f"fish_quest_{count}_of_5.png")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "Media/IMG_1083.MOV")
    parser.add_argument("--reference", type=Path, default=ROOT / "Media/mackerel_final_v24.mp4")
    parser.add_argument("--dialogue", type=Path, default=ROOT / "Media/mackerel_v24_dialogue.wav")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--font", type=Path,
                        default=Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts/consolab.ttf")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True)
    clips = output / "Clips"
    audio = output / "Audio"
    graphics = output / "Graphics"
    for folder in (clips, audio, graphics):
        folder.mkdir()

    draw_counter(graphics, args.font)
    with (output / "source_cuts.csv").open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(("clip", "source_in_seconds", "source_out_seconds", "review_note"))
        writer.writerows(CANDIDATES)

    for name, source in (
        ("v24_intro_reference_mix", args.reference),
        ("v24_intro_clean_dialogue", args.dialogue),
    ):
        ffmpeg("-i", source, "-t", f"{607 / 30:.9f}", "-map", "0:a:0",
               "-c:a", "pcm_s24le", audio / f"{name}.wav")

    for name, start, end, _ in CANDIDATES:
        print(f"Exporting {name}", flush=True)
        ffmpeg("-ss", start, "-threads", 4, "-i", args.source.resolve(),
               "-t", round(end - start, 3), "-map", "0:v:0", "-map", "0:a:0",
               "-filter_threads", 2, "-vf", "fps=30,scale=1080:1920:flags=lanczos,setsar=1",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", 20, "-threads", 4,
               "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
               "-colorspace", "bt709", "-c:a", "aac", "-b:a", "256k",
               "-movflags", "+faststart", clips / f"{name}.mp4")


if __name__ == "__main__":
    main()
