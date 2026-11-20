"""Deliver the bundled news-image artwork to the output directory.

The artwork is pre-drawn and shipped as ``entry.png`` beside this
file; this program's only job is to deliver those exact bytes to the
contest runner's output location, deterministically:

  * Destination: ``$MAKEFUN_OUTPUT_DIR`` if set and non-empty,
    otherwise ``/output``; the directory is created if needed.
  * The bundled file is checked against the 8-byte PNG signature
    before writing, so missing/corrupt artwork fails loudly.
  * After writing, the file is read back, compared byte-for-byte
    with the bundled bytes, and re-checked for the signature.

Standard library only, no network. The repository may be read-only;
the only write is to the output directory.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# The 8-byte magic number that begins every PNG file.
PNG_SIGNATURE = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))

ARTWORK_NAME = "entry.png"
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"


def artwork_path() -> Path:
    """Return the path of the artwork bundled beside this file."""
    return Path(__file__).resolve().parent / ARTWORK_NAME


def resolve_output_dir() -> Path:
    """Return the output dir: env var if set/non-empty, else default."""
    configured = os.environ.get(OUTPUT_ENV_VAR, "").strip()
    if configured:
        return Path(configured)
    return Path(DEFAULT_OUTPUT_DIR)


def check_png_signature(data: bytes, origin: str) -> None:
    """Raise ValueError unless *data* starts with the PNG signature."""
    if len(data) < len(PNG_SIGNATURE):
        raise ValueError(f"{origin}: too short to be a PNG ({len(data)} bytes)")
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError(f"{origin}: missing PNG signature")


def read_artwork(source: Path) -> bytes:
    """Read the bundled artwork and verify that it is a PNG."""
    if not source.is_file():
        raise FileNotFoundError(f"bundled artwork not found: {source}")
    data = source.read_bytes()
    check_png_signature(data, f"bundled artwork {source}")
    return data


def deliver(data: bytes, output_dir: Path) -> Path:
    """Write *data* into *output_dir* and verify the written file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / ARTWORK_NAME
    destination.write_bytes(data)
    # Read back what landed on disk; it must match exactly.
    written = destination.read_bytes()
    check_png_signature(written, f"written file {destination}")
    if written != data:
        raise RuntimeError(
            f"verification failed: {destination} differs from bundled artwork"
        )
    return destination


def main() -> int:
    """Copy the bundled artwork to the output directory."""
    data = read_artwork(artwork_path())
    destination = deliver(data, resolve_output_dir())
    print(f"Delivered {ARTWORK_NAME} ({len(data)} bytes) to {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
