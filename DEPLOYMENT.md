# Stable Studionet deployment evidence

**STATUS: BLOCKED / INCOMPLETE — no live deployment or transaction evidence.**

The installed GenLayer CLI (`0.39.1`) reports the effective alias `studionet`, chain ID `61999`, RPC `https://studio.genlayer.com/api`. The stable network configuration matches the required target. A direct read-only JSON-RPC `eth_chainId` request could not run: this environment denies outbound sockets. No deployment or write was attempted.

| Evidence | Result |
| --- | --- |
| SubstituteX address and deployment transaction | Not deployed |
| SubstitutionGate address and deployment transaction | Not deployed |
| Role ID, definition hash, proposal ID, finding transactions, certificate hash | Not generated onchain |
| Gated action, replay rejection and successor invalidation | Not demonstrated onchain |
| Stable RPC-reported chain ID | Not queried; outbound socket denied |
| Required explorer | [Studionet explorer](https://explorer-studio.genlayer.com) |
| Immutable fixture commit SHA and URLs | Not published or pinned |
| Direct Mode | `pytest tests/direct -v`: 20 passed (mocked local runtime) |

Do not treat Direct Mode as proof of network compatibility, transaction finality, source fetch behavior on GenVM, or live cross-contract execution. Fill this record only from actual Studionet receipts and explorer evidence.
