#!/usr/bin/env python3
"""Entry program for news-image-20261122.

Writes the front-page image that sums up Sunday 22 November 2026 to
the output directory. The image itself is entry.png, drawn at build
time by draw.py (Pillow, build time only); this program uses only the
standard library, so it runs in the grader's sandbox with no network
and no third-party packages. Copying fixed bytes is deterministic:
every run writes the same file.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print("entry.png is missing from the repository", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    print("wrote", target, os.path.getsize(target), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
