"""Entrypoint: render the 23 November 2026 front page to entry.png.

Stdlib only. No network, no clock, no randomness — every run writes the
same bytes. The output directory comes from MAKEFUN_OUTPUT_DIR, falling
back to /output (the sandbox path) when the variable is unset.
"""

import os

import frontpage
from news_data import DATA


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    canvas = frontpage.render(DATA)
    png = frontpage.encode_png(canvas)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as fh:
        fh.write(png)
    print("wrote %s (%d bytes)" % (path, len(png)))


if __name__ == "__main__":
    main()
