# SubstituteX — Role-scoped functional substitutability on GenLayer

A **standalone reusable Intelligent Contract primitive**, not an app. It certifies whether a different replacement can perform a particular role for an original **under an immutable set of invariants**. Proof is asymmetric (`A → B` does **not** imply `B → A`), role-specific, expiring and version-pinned.

This is *not* an identity merge, agreement equivalence checker, simple natural-language permission contract, escrow, matching market, or ranking oracle. Other contracts query a pinned certification and enforce their own actions.

## Contract files

- `contracts/substitutex.py`: roles, invariant groups, source namespace, independent two-source semantic assessments, deterministic certificates and version validity.
- `contracts/substitution_gate.py`: separate consumer with typed IC-to-IC read and one-time action-hash replay protection.
- `fixtures/`: fictional source paragraphs for testing; require publication under a real pinned GitHub commit before live tests.
- `scripts/preflight.py`: offline source structure and final evidence-shape gate.
- `scripts/pin_fixture_commit.py`: writes public raw source URLs for a supplied full Git commit SHA.
- `scripts/studionet_write.py`: verifies the active stable Studionet alias and RPC chain ID before a write, then waits for a finalized receipt.

## Protocol quick view

```text
Role OPEN --add prefixes / invariants--> SEALED [definition_hash]
  |                                    |
  |                                Proposal A → B [expires_at]
  |                                    |
  |                   per-invariant: independently refetched two-source consensus
  |                                    |
  |              PRESERVED / VIOLATED / AMBIGUOUS / UNAVAILABLE
  |                                    |
  |               deterministic ALL/ANY/OPTIONAL/PROHIBITION aggregation
  |                                    |
  |                           CERTIFIED / REJECTED
  |                                    |
  |                     64-hex scoped certificate_hash
  |                                    |
  |              SubstitutionGate exact pinned read + replay prevention
  |
  +--new separately sealed successor role--> old certificates historical but inactive
```

## Requirements

Use Python 3.12+ and the stable GenLayer SDK/test family compatible with Studionet. Start:

```bash
python scripts/preflight.py
python -m compileall -q contracts tests scripts
python -m pip install -r requirements-test.txt
pytest tests/unit -v
pytest tests/direct -v
```

The stable Direct Mode suite uses `genlayer-test 0.29.2`, `genlayer-py 0.16.3`, and the contracts' declared `py-genlayer` dependency. The direct tests pin the matching `v0.2.12` runtime to avoid selecting a cached preview artifact, and include a Windows stdin-cleanup workaround for the test runner. The fixture URLs are pinned to the first published commit and all four URLs were fetched successfully and compared with the repository fixture contents.

## Network lock

- Target: `studionet`
- Chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- Explorer: `https://explorer-studio.genlayer.com`

Do not migrate to `studio-dev` (61997), Asimov, Bradbury or localnet for the final proof. Local Direct Mode can be used for tests without a chain.

## Usage and typed interface

Create a role, add source prefixes and invariants, seal, propose, assess each invariant via consensus, finalize, and read:

```python
SubstituteX.is_substitutable(proposal_id, expected_role_hash,
    expected_certificate_hash, original_key, replacement_key)
```

For detailed invariants, group behavior, threat model, and test scenario see `docs/`.

## Important security semantics

Verdicts describe the two **fetched published descriptions** for an individual declared requirement. A `PRESERVED` verdict is *not* universal product safety, truth of all vendor claims, or a legal/compliance guarantee. The model must not set final certification. Optional failures appear in `get_composition` but do not invalidate mandatory coverage. `UNAVAILABLE` or `AMBIGUOUS` for mandatory invariants prevents certification.

The frozen host/path prefixes are user-specified; only choose trusted source authorities. `gl.nondet.web.get` response/redirect behavior must be validated on the actual stable runtime. Certificates expire and earlier role versions lose active authorization when successors seal.

## Status

**Live stable Studionet lifecycle completed; final repository checks are recorded in `BUILD_STATUS.md`.** SubstituteX and SubstitutionGate were deployed on chain 61999. The immutable role and five independent findings produced one certified good candidate and one rejected bad candidate. The deployed Gate made a real typed cross-contract view call, recorded one pinned action, and rejected replay, wrong certificate, reversed identities, and a historical certificate after a successor was sealed. Addresses, transaction hashes and explorer links are in `deployments/studionet.json`; detailed evidence and limitations are in `DEPLOYMENT.md` and `SUBMISSION.md`.
