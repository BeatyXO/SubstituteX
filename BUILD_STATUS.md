# Build status

## Verified locally

- Python 3.12.10; GenLayer CLI 0.39.1; `genlayer-test` 0.29.2; `genlayer-py` 0.16.3.
- The contract `py-genlayer` dependency is pinned to the matching stable `v0.2.12` artifact for Direct Mode tests.
- `python scripts/preflight.py`: passed.
- `python -m compileall -q contracts scripts tests`: passed.
- `pytest tests/unit -v`: 26 passed.
- `pytest tests/direct -v`: 20 passed, including a mocked validator disagreement, source snapshot mutation, expiry boundary, fail-closed unavailable/oversized sources, policy groups, prohibition veto, and typed Gate call through the Direct Mode cross-contract hook.
- `genlayer network info`: reports `studionet`, chain ID 61999 and the required RPC.

## Blocked release gates

No live stable Studionet transaction was submitted. The environment denies outbound sockets, so `eth_chainId` could not be read and GitHub could not be inspected or pushed. The public fixture commit SHA is therefore unknown, fixture URLs remain unpinned, and neither contract has a live address. This repository is **INCOMPLETE and not submission ready** until public publication, stable RPC verification, live deployment, lifecycle proofs and final remote audit succeed.
