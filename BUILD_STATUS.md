# Build status

## Final local checks

- Python 3.12.10; GenLayer CLI 0.39.1; `genlayer-test` 0.29.2; `genlayer-py` 0.16.3.
- Contract testing dependency is pinned to stable `v0.2.12` for Direct Mode.
- `python scripts/preflight.py`: passed.
- `python scripts/preflight.py --final`: passed, including the deployment evidence shape and immutable fixture URL checks.
- `python -m compileall -q contracts scripts tests`: passed.
- `pytest tests/unit -q`: 26 passed.
- `pytest tests/direct -q`: 22 passed, including independent validator assessment, forged leader verdict rejection, source snapshot mutation, expiry boundary, unavailable and oversized sources, invariant composition, prohibition veto, and typed Gate behavior.
- `SUBSTITUTEX_CHECK_PICKLING=1 pytest tests/direct -q`: 22 passed with GenLayer Direct Mode pickling checks enabled.

## Stable Studionet

- `genlayer network info` reported alias `studionet`, chain ID 61999 and RPC `https://studio.genlayer.com/api`.
- The RPC `eth_chainId` returned `0xf22f` (61999). The network was reverified before each deployment and write workflow.
- Both contracts were deployed and finalized. The positive certification, rejected substitution, typed Gate execution, replay rejection, invalid certificate and successor invalidation transactions are documented with real hashes and explorer links in [`deployments/studionet.json`](deployments/studionet.json).
- Public fixture URLs are pinned to immutable commit `246a12ceb2ae1a8b4b643b99a5153868fff99c43`; all four returned HTTP 200 and matched their checked-in fixture contents.

## Evidence limits

- Live expiry was not awaited; the exact expiry-boundary behavior is covered by Direct Mode time-warp tests.
- Stable Studionet does not expose the CLI trace RPC method used here. Finalized receipts and explorer transaction details were used for live evidence.
- The RPC intermittently returned an HTML gateway response instead of JSON. Affected transaction hashes were captured and receipts checked later; no transaction was blindly resubmitted.
- A validator-disagreement assessment finalized without changing state. Its majority-agree retry was accepted and the proposal was certified.

The final full Git commit SHA is reported after pushing and verifying the remote `main` branch.
