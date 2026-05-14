#!/usr/bin/env python3
"""Toggle Dave's tracker color between red (Vader) and blue (Anakin)."""

import re
import sys
from pathlib import Path

HTML = Path(__file__).resolve().parents[2] / "index.html"

PAIRS = {"red": "blue", "blue": "red"}
LABELS = {"red": "Vader red", "blue": "Anakin blue"}


def safelist_classes(color: str) -> str:
    return (
        f"bg-{color}-600 bg-{color}-950/50 border-{color}-800 "
        f"border-{color}-400 border-{color}-500 text-{color}-300 "
        f"text-{color}-400 shadow-{color}-600/30 shadow-{color}-600/40"
    )


def main() -> int:
    content = HTML.read_text()

    if "renderMovementTracker('dave', 'red')" in content:
        old, new = "red", "blue"
    elif "renderMovementTracker('dave', 'blue')" in content:
        old, new = "blue", "red"
    else:
        print("ERROR: could not detect Dave's current color", file=sys.stderr)
        return 1

    content = re.sub(
        r'(<img src="Dave\.png" alt="Dave" class="[^"]*border-)' + old + r'(-500[^"]*">)',
        r"\1" + new + r"\2",
        content,
    )
    content = re.sub(
        r'(<h2 class="text-2xl font-bold text-)' + old + r'(-400">Dave)',
        r"\1" + new + r"\2",
        content,
    )
    content = content.replace(
        f"renderMovementTracker('dave', '{old}')",
        f"renderMovementTracker('dave', '{new}')",
    )
    content = content.replace(safelist_classes(old), safelist_classes(new))

    HTML.write_text(content)
    print(f"Swapped Dave: {LABELS[old]} -> {LABELS[new]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
