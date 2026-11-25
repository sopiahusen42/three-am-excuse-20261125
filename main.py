"""Write the entry line for the make.fun bounty "The 3 AM Excuse".

The bounty asks for one line, under 200 characters, giving the most creative
excuse a hardware wallet makes for refusing to sign a transaction at 3 a.m.
ENTRY holds that line verbatim. This program validates it, writes it plus a
single trailing newline to entry.txt as UTF-8, and reads the file back to
confirm the bytes on disk are exactly what was intended.

The program is deterministic: it reads no clock, uses no randomness, takes no
network, and writes the same bytes on every run. The only input it consults is
the optional MAKEFUN_OUTPUT_DIR environment variable, which selects the output
directory and defaults to /output. Success is silent with exit status 0; any
validation or write-verification failure prints one line to stderr and exits 1.
"""

import os
import sys

ENTRY = (
    "It is 3 a.m. Your last three signatures at this hour were rent, "
    "revenge and a token called probably-fine. Come back with coffee."
)


def validate_entry(text: object) -> str | None:
    """Return an error message for an invalid entry, or None when it is valid."""
    if not isinstance(text, str):
        return "entry: not a string"
    if not text.strip():
        return "entry: blank"
    if len(text) < 1 or len(text) > 200:
        return "entry: length outside 1..200 code points"
    if "\n" in text or "\r" in text:
        return "entry: contains a line break"
    if text != text.strip():
        return "entry: has leading or trailing whitespace"
    return None


def main() -> int:
    error = validate_entry(ENTRY)
    if error is not None:
        print(error, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    payload = ENTRY + "\n"
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(payload)

    with open(out_path, "r", encoding="utf-8", newline="") as handle:
        on_disk = handle.read()
    if on_disk != payload:
        print("entry.txt: bytes on disk differ from intended payload", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
