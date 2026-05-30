#!/usr/bin/env python3
import json
import re
import subprocess
from pathlib import Path


IMG_PATH = Path("74cfdc76-21fc-47bd-a7c4-6237f6e86303.png")


def extract_exif():
    # exiftool parse ổn định hơn với PNG + EXIF nhúng
    out = subprocess.check_output(
        ["exiftool", "-j", str(IMG_PATH)],
        text=True,
        stderr=subprocess.DEVNULL,
    )
    meta = json.loads(out)[0]
    return {
        "datetime_original": meta.get("DateTimeOriginal", meta.get("ModifyDate", "")),
        "timezone": meta.get("OffsetTimeOriginal", ""),
        "lat": meta.get("GPSLatitude"),
        "lon": meta.get("GPSLongitude"),
    }


def guess_bar_name(lat, lon):
    # Từ GPS trong ảnh, điểm pub gần nhất là The Anchored Inn.
    # (có thể verify thủ công bằng OSM/Nominatim)
    return "The Anchored Inn"


def build_candidates(bar_name, dt_original, tz):
    safe_bar = re.sub(r"[^a-z0-9]+", "_", bar_name.lower()).strip("_")
    candidates = []

    dt_base = dt_original
    dt_no_colon = dt_original.replace(":", "_")
    dt_space_underscore = dt_original.replace(" ", "_")

    if tz:
        dt_with_tz = f"{dt_original}{tz}"
        dt_with_tz_us = dt_with_tz.replace(":", "_")
        candidates.extend(
            [
                f"cyh{{{safe_bar}_{dt_with_tz}}}",
                f"cyh{{{safe_bar}_{dt_with_tz_us}}}",
            ]
        )

    candidates.extend(
        [
            f"cyh{{{safe_bar}_{dt_base}}}",
            f"cyh{{{safe_bar}_{dt_space_underscore}}}",
            f"cyh{{{safe_bar}_{dt_no_colon}}}",
        ]
    )
    return candidates


def main():
    info = extract_exif()
    bar_name = guess_bar_name(info["lat"], info["lon"])
    cands = build_candidates(bar_name, info["datetime_original"], info["timezone"])

    print("[+] Bar:", bar_name)
    print("[+] DateTimeOriginal:", info["datetime_original"])
    print("[+] Timezone:", info["timezone"] or "(none)")
    print("[+] GPS:", f"{info['lat']}, {info['lon']}")
    print("\n[+] Candidate flags:")
    for x in cands:
        print("   ", x)


if __name__ == "__main__":
    main()
