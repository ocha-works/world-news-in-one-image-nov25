#!/usr/bin/env python3
"""Entry point for the news-image-20261125 make.fun bounty.

Validates the bundled entry.png (a whole, well-formed PNG within the
competition limits) and copies it byte-for-byte to the output directory
given by MAKEFUN_OUTPUT_DIR (default /output/entry.png).

Standard library only. No network access.
"""
import os
import struct
import sys
import zlib

MAX_BYTES = 1_048_576
MAX_DIM = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    return 1


def validate_png(data):
    """Check the whole PNG: magic, IHDR dims, every chunk CRC, IEND."""
    if len(data) > MAX_BYTES:
        return f"file is {len(data)} bytes, over the {MAX_BYTES} byte limit"
    if len(data) < 8 or data[:8] != PNG_MAGIC:
        return "not a PNG file (bad magic bytes)"

    pos = 8
    seen_ihdr = False
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            return "truncated chunk header"
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + length > len(data):
            return f"truncated chunk {ctype!r}"
        chunk_data = data[pos + 8:pos + 8 + length]
        crc_stored = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
        crc_actual = zlib.crc32(ctype)
        crc_actual = zlib.crc32(chunk_data, crc_actual)
        if crc_actual != crc_stored:
            return f"bad CRC in chunk {ctype!r}"
        if ctype == b"IHDR":
            if seen_ihdr:
                return "duplicate IHDR chunk"
            if length != 13:
                return "bad IHDR length"
            width, height = struct.unpack(">II", chunk_data[:8])
            if width > MAX_DIM or height > MAX_DIM:
                return f"image is {width}x{height}, over the {MAX_DIM}x{MAX_DIM} limit"
            if width == 0 or height == 0:
                return "image has a zero dimension"
            seen_ihdr = True
        if ctype == b"IEND":
            if length != 0:
                return "bad IEND length"
            seen_iend = True
            pos += 12 + length
            break
        pos += 12 + length

    if not seen_ihdr:
        return "missing IHDR chunk"
    if not seen_iend:
        return "missing IEND chunk (truncated file)"
    if pos != len(data):
        return "trailing data after IEND"
    return None


def main():
    try:
        with open(SOURCE, "rb") as f:
            data = f.read()
    except OSError as exc:
        return fail(f"cannot read bundled entry.png: {exc}")

    problem = validate_png(data)
    if problem is not None:
        return fail(f"invalid entry.png: {problem}")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.png")
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(data)
    except OSError as exc:
        return fail(f"cannot write {out_path}: {exc}")

    print(f"wrote {out_path} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
