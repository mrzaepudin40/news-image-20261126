#!/usr/bin/env python3
"""Entry for make.fun bounty news-image-20261126.

Writes the image that sums up the world's news of Thursday
26 November 2026 to /output/entry.png.

The image is a broadsheet drawn for this bounty: masthead with the
date, two lead stories (US tariff rates on 14 economies; Kim Jong
Un calling North Korea's nuclear expansion irreversible), six
regional stories, and a timeline of the day. It is stored in this
repository as entry.png (1024x1024, under 1 MiB).

Standard library only, no network, fully deterministic: every run
copies the same bytes to the same path.
"""

import os
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"

MAX_BYTES = 1_048_576  # 1 MiB, the bounty cap
EXPECTED_SIZE = (1024, 1024)


def validate_png(path: Path) -> None:
    """Check the bundled image meets the bounty limits, stdlib only.

    Verifies the PNG signature, the IHDR dimensions (1024x1024) and
    the 1 MiB size cap, so a bad asset fails loudly instead of
    submitting an invalid entry.
    """
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise SystemExit(f"image asset too large: {len(data)} bytes")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("image asset is not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise SystemExit("image asset has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != EXPECTED_SIZE:
        raise SystemExit(f"image asset is {width}x{height}, want 1024x1024")


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"missing image asset: {SOURCE}")
    validate_png(SOURCE)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    if target.stat().st_size != SOURCE.stat().st_size:
        raise SystemExit("copied image size does not match the asset")
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
