# Stable Studionet deployment evidence

**STATUS: BLOCKED / INCOMPLETE — no live deployment or transaction evidence.**

The installed GenLayer CLI (`0.39.1`) reports alias `studionet`, chain ID `61999`, and RPC `https://studio.genlayer.com/api`. A read-only `eth_chainId` request to that endpoint returned `0xf22f` (61999). No deployment or write was attempted because the fixtures cannot be pinned until the initial repository push succeeds.

| Evidence | Result |
| --- | --- |
| SubstituteX address and deployment transaction | Not deployed |
| SubstitutionGate address and deployment transaction | Not deployed |
| Role ID, definition hash, proposal ID, finding transactions, certificate hash | Not generated onchain |
| Gated action, replay rejection and successor invalidation | Not demonstrated onchain |
| Stable RPC-reported chain ID | `0xf22f` (61999), read-only RPC response |
| Required explorer | [Studionet explorer](https://explorer-studio.genlayer.com) |
| Immutable fixture commit SHA and URLs | Not published or pinned |
| Direct Mode | `pytest tests/direct -v`: 21 passed (mocked local runtime) |

The initial GitHub push was rejected with HTTP 403: GitHub authenticated the request as `Ifem1` and denied permission to `BeatyXO/SubstituteX`. The remote was verified empty before the push. The local commits are preserved on `main`; no public immutable fixture URLs or live fixture proof exist yet.

Do not treat Direct Mode as proof of network compatibility, transaction finality, source fetch behavior on GenVM, or live cross-contract execution. Fill this record only from actual Studionet receipts and explorer evidence.
