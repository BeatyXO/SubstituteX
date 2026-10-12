#!/usr/bin/env python3
"""Offline structure/security preflight; no deployment or finality claims."""
from pathlib import Path
import argparse
import ast
import re
import sys
import subprocess

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [
    "contracts/substitutex.py", "contracts/substitution_gate.py", "README.md",
    "SUBMISSION.md", "DEPLOYMENT.md", "docs/ARCHITECTURE.md",
    "docs/INVARIANTS.md", "docs/SECURITY.md", "tests/unit/test_contract_helpers.py",
    "tests/direct/test_substitutex.py", "requirements-test.txt", "gltest.config.yaml",
]
BAD_PATH_PARTS = {".env", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", "secrets", "dist"}


def run(final: bool) -> list[str]:
    errors = []
    for path in EXPECTED:
        if not (ROOT / path).is_file():
            errors.append("missing " + path)
    # Only tracked files are dangerous in a checkout. Ignored local test caches
    # must not make --final fail immediately after pytest/compileall runs.
    tracked: list[Path] = []
    if (ROOT / ".git").exists():
        try:
            res = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True)
            tracked = [Path(x.decode()) for x in res.stdout.split(b"\x00") if x]
        except (OSError, subprocess.CalledProcessError):
            errors.append("cannot inspect tracked files")
    for rel in tracked:
        if any(bit in BAD_PATH_PARTS or bit.endswith((".pyc", ".pem", ".key")) for bit in rel.parts):
            errors.append("prohibited tracked file " + str(rel))
    for path in (ROOT / "contracts").glob("*.py"):
        src = path.read_text()
        try:
            ast.parse(src)
        except SyntaxError as exc:
            errors.append(f"invalid Python {path.name}: {exc}")
        if not src.startswith('# { "Depends": "py-genlayer:'):
            errors.append("missing pinned GenVM dependency: " + path.name)
    config = (ROOT / "gltest.config.yaml").read_text()
    if "https://studio.genlayer.com/api" not in config:
        errors.append("stable Studionet RPC missing from gltest config")
    if "61999" not in (ROOT / ".env.example").read_text():
        errors.append("stable chain ID marker missing")
    if final:
        pin = ROOT / "deployments" / "fixture_pin.json"
        if not pin.is_file():
            errors.append("missing pinned immutable public fixture manifest")
        else:
            import json
            data = json.loads(pin.read_text())
            if not re.fullmatch(r"[0-9a-f]{40}", data.get("commit_sha", "")):
                errors.append("invalid fixture commit SHA")
        evidence = ROOT / "deployments" / "studionet.json"
        if not evidence.is_file():
            errors.append("missing deployment evidence record")
        else:
            import json
            item = json.loads(evidence.read_text())
            if item.get("network") != "studionet" or item.get("chain_id") != 61999:
                errors.append("live deployment evidence must target stable chain 61999")
            if not item.get("substitutex_address") or not item.get("gate_address"):
                errors.append("final deployment addresses not recorded")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    issues = run(args.final)
    for issue in issues:
        print("FAIL:", issue)
    if issues:
        sys.exit(1)
    print("PASS: offline preflight" + (" (final evidence shape)" if args.final else ""))
