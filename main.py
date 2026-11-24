"""NI23 v2 entrypoint: renders Monday 23 November 2026's one-page news image."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from draw import render


def out_path():
    if os.path.isdir("/output") and os.access("/output", os.W_OK):
        return "/output/entry.png"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    canvas, total, counts, _ = render()
    data = canvas.png_bytes()
    assert len(data) <= 1048576 and data[:8] == b"\x89PNG\r\n\x1a\n"
    path = out_path()
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, path)
    print("stories", total, sorted(counts.items()), "bytes", len(data))


if __name__ == "__main__":
    main()
