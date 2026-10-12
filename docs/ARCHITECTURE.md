# Architecture

## Boundary

SubstituteX certifies **directed**, **role-scoped** substitution from an original to a distinct replacement. It is not an identity merger, semantic ranking, licence inheritance, source-corroboration engine, or escrow. No frontend, token, governance, or offchain indexer is needed to use the primitive.

## Objects

- `Role`: author, purpose, monotonically versioned successor, frozen HTTPS source prefix allowlist, frozen invariant set, canonical definition hash.
- `Invariant`: semantic requirement with `REQUIRED`, `OPTIONAL`, or `PROHIBITION` kind. Required invariants may belong to explicit `ALL`/`ANY` groups.
- `Proposal`: directed `(original_key, replacement_key)`, distinct immutable source URLs, frozen role hash, expiry, per-invariant assessment count, final status.
- `Finding`: one consensus-backed, immutable assessment of a single invariant against the two fetched source texts. Source digests and decisive evidence quotes are stored. Every finding in a proposal must refer to the **same pair of source digests**; mixed-version snapshots revert.
- `Certificate`: deterministic hash of role definition, directed identities, expiry, and *ordered* finding hashes. A certificate is authorized only while role is current and not expired.

## Division of labor

**Nondeterministic:** web.get the original and replacement descriptions, prompt the LLM about exactly one invariant, obtain `PRESERVED`, `VIOLATED`, `AMBIGUOUS`, or `UNAVAILABLE`; validator independently refetches and re-runs this task. For decisive outcomes, quotes must exist verbatim in **both fetched texts**. The validator compares verdict and both source digests and checks independently fetched grounding for leader quotes. External documents remain untrusted data, never instructions.

**Deterministic:** creator permissions, prefix URL boundaries, sealing, definition hashing, proposal admission, one-time assessment per invariant, group composition, hard failure on prohibited behavior, certificate construction, expiry, directed identity binding, successor invalidation and consumer execution replay protection.

## Group composition

- Ungrouped REQUIRED and PROHIBITION: `PRESERVED` needed.
- REQUIRED group `ALL`: every member PRESERVED.
- REQUIRED group `ANY`: at least one PRESERVED; if none and at least one unknown, unresolved; if all VIOLATED, rejected.
- OPTIONAL: evaluated and reported but cannot veto certification.
- PROHIBITION: model must classify whether the replacement introduces banned behavior; VIOLATED vetoes certification.
- Any missing result, AMBIGUOUS, or UNAVAILABLE in a mandatory slot leaves candidate noncertifiable. The model cannot declare the overall status.

## Role version semantics

A version is a new, separately sealed Role pointing back to its sealed predecessor and owned by the same address. When it seals, predecessor `successor_id` is set. Predecessor certificates remain queryable in historical records but `is_substitutable` returns false. No automatic migration. Only one direct successor is permitted.

## Consumer

`SubstitutionGate.execute_replacement` calls `ISubstituteX(...).view().is_substitutable(proposal_id, expected_role_hash, expected_certificate_hash, original_key, replacement_key)` and records a unique action hash. This blocks wrong-role replay, wrong-certificate replay, inverse-direction replay, expired/superseded certificates, and same-action replay. This is a demo of composability, not a production asset custodian.

## Limitations requiring live validation

- External providers can update or remove URL content; certificate assessment is a snapshot, not a real-time guarantee. Immutable pinned GitHub fixtures demonstrate repeatability; future policies may adopt mandatory refresh snapshots.
- An LLM may make a wrong substantive classification despite independent validators. Ambiguity, unsupported claims and missing sources should fail closed.
- Direct Mode/Studionet may differ in transaction-time availability and web fetching behavior; test explicitly.
- Direct Mode's typed consumer test routes the GenVM `CallContract` request through the test suite hook. It verifies the consumer's ABI call shape and state guard, but does not replace a live two-contract Studionet transaction. The local runner's single-contract storage context prevented composing two deployed instances in one Direct Mode VM.
