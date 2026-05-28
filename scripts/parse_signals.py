"""
parse_signals.py — read all markdown signal files in signals/, extract YAML
frontmatter and notes body, emit a single signals.json for the dashboard.

Usage: python scripts/parse_signals.py
Output: data/signals.json
"""
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml --break-system-packages")
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
SIGNALS_DIR = ROOT / "signals"
OUT_FILE = ROOT / "data" / "signals.json"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_signal_file(path: Path) -> dict:
    """Parse a single signal markdown file."""
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"{path.name}: missing YAML frontmatter")

    frontmatter_text, body = m.group(1), m.group(2).strip()
    data = yaml.safe_load(frontmatter_text)

    # Normalise dates to ISO strings (yaml may auto-parse to date objects)
    if "signal_date" in data:
        data["signal_date"] = str(data["signal_date"])
    if "lookback_start" in data:
        data["lookback_start"] = str(data["lookback_start"])

    data["notes_markdown"] = body
    data["source_filename"] = path.name
    return data


def main():
    files = sorted(SIGNALS_DIR.glob("*.md"))
    if not files:
        print(f"No signal files found in {SIGNALS_DIR}")
        return

    signals = []
    for f in files:
        try:
            signals.append(parse_signal_file(f))
            print(f"  parsed {f.name}")
        except Exception as e:
            print(f"  FAILED {f.name}: {e}")

    OUT_FILE.parent.mkdir(exist_ok=True)
    OUT_FILE.write_text(json.dumps(signals, indent=2), encoding="utf-8")
    print(f"\nWrote {len(signals)} signals to {OUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
