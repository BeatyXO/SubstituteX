#!/usr/bin/env python3
"""Pin raw fixture URLs to a supplied, externally verified, FULL Git commit."""
import json
import re
import sys
from pathlib import Path

if len(sys.argv) != 2 or not re.fullmatch(r"[0-9a-f]{40}", sys.argv[1]):
    raise SystemExit("Usage: python scripts/pin_fixture_commit.py <full-40-character-commit-sha>")
sha = sys.argv[1]
prefix = "https://raw.githubusercontent.com/BeatyXO/SubstituteX/" + sha + "/fixtures/"
files = ("original_provider.txt", "replacement_good.txt", "replacement_bad.txt", "replacement_unknown.txt")
root = Path(__file__).resolve().parents[1]
payload = {"commit_sha": sha, "source_prefix": prefix, "urls": {x: prefix + x for x in files},
           "note": "Generator does not confirm GitHub publication. Verify every immutable URL before live use."}
path = root / "deployments" / "fixture_pin.json"
path.write_text(json.dumps(payload, indent=2) + "\n")
print("Written:", path, "(publication not verified)")
