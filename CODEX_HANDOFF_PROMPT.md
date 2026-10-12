# SubstituteX — Codex takeover and final-delivery prompt

You are taking over a **substantially implemented but not yet runtime-verified** GenLayer Intelligent Contract repository named **SubstituteX**. The code has been bundled in a ZIP; unzip it first, read its contents and finish the work **in the existing directory**. Do not return only a plan, mockup, checklist, general advice, or a renamed boilerplate. Execute the remaining engineering, testing, on-chain verification and repository publication where the required access exists.

**GITHUB DESTINATION**

- Repository: **https://github.com/BeatyXO/SubstituteX.git**
- Owner/repo: **BeatyXO/SubstituteX**
- Default branch: **main**
- The repository was just created and may be empty. Initialize Git in the unzipped project if necessary, configure `origin` exactly to the URL above, commit the actual code and push **without force-pushing**. Verify current remote contents before and after. Do not accidentally push to an older project/owner. If local credentials cannot push, preserve the completed local commits and report the concrete authentication/permissions blocker; never claim a push that did not happen.

## PRODUCT BOUNDARY — non-negotiable

SubstituteX is a standalone, reusable **GenLayer Intelligent Contract primitive**, not a full application. **No frontend**. No token or escrow machinery. No unrelated governance apparatus.

The primitive answers one tightly scoped question:

> Can a different candidate B substitute for original A **for this declared role** while preserving the role's sealed invariants?

This is **purpose-scoped and asymmetric**. `A → B` never implies `B → A`. The contract **does not** merge identities, rank alternatives, semantically lock agreement wording, count independent evidence, reason about causal attribution, propagate licences, schedule jobs, or perform permission inheritance.

The core architecture MUST survive:

1. `Role`: owner, role purpose, bounded trusted HTTPS source prefixes, bounded typed invariant definitions, immutable `definition_hash` after seal, monotonic successor versioning.
2. `Invariant`: `REQUIRED`, `OPTIONAL`, `PROHIBITION`; the required slots may use explicit `ALL`/`ANY` group rules. There is at least one mandatory requirement. All group semantics are deterministic and committed before assessment.
3. `Proposal`: binds one directed original/replacement pair to the current sealed role, two distinct immutable source URLs, expiry, frozen role hash and independent per-invariant findings.
4. `Finding`: individual consensus-backed verdict: `PRESERVED`, `VIOLATED`, `AMBIGUOUS` or `UNAVAILABLE`, with short verbatim snippets grounded in both independently fetched source documents for decisive outcomes, stable source digests, and finding hashes.
5. **A single proposal may not combine contradictory source snapshot digests across its findings.** This prevents stale/mutable content from being mixed into one certificate.
6. Overall `CERTIFIED` or `REJECTED` is produced **only by deterministic code** over the findings and precommitted group policy. The model must NEVER choose overall approval.
7. `certificate_hash` commits to role hash, directed original/replacement identities, expiry and ordered finding hashes. Historical certificates remain queryable, but `is_substitutable()` returns false after expiry or when that role gets a newly sealed successor.
8. The `SubstitutionGate` is a real second Intelligent Contract that does a **typed cross-contract view call**, requires the exact role and certificate hash and both identity keys, and rejects repeated `action_hash` executions.

Do not collapse SubstituteX into `LLM says replacement is safe: true/false`, a generic compatibility classifier or a frontend demo. Preserve genuine non-AI protocol depth.

## NON-NEGOTIABLE NETWORK

For any **live** deployment or read/write proof:

- Network alias: `studionet`
- Chain ID: **61999**
- GenLayer RPC: **https://studio.genlayer.com/api**
- Explorer: **https://explorer-studio.genlayer.com**

Before **each** deploy/write workflow use the installed CLI's supported network-info / RPC checks and verify effective chain ID **61999**. Do NOT silently use `studio-dev` (61997), another testnet, or a local chain as substitution. Direct Mode/in-memory tests are allowed locally. When fees require estimation, use the **supported stable Studionet** fee method, never a network switch. Confirm the actual stable package/tooling versions against the official GenLayer docs before modifying pins, and record any justified changes.

## MANDATORY READ AND FIRST CHECKS

1. Read `README.md`, `SUBMISSION.md`, `DEPLOYMENT.md`, `BUILD_STATUS.md`, **all** docs, both contracts, all tests, fixtures, CLI configs, scripts, CI workflow and this handoff document **before editing**.
2. Run `python scripts/preflight.py` immediately, then `python -m compileall -q contracts scripts tests` and `pytest tests/unit -v`.
3. Install the repository's test dependencies (`requirements-test.txt`) on Python **3.12+**. Run **all** Direct Mode tests `pytest tests/direct -v`. Run `direct_vm.check_pickling = True` for important lifecycle tests if supported.
4. Fix genuine compatibility errors and failing behavior. Do not weaken/delete tests to manufacture green results. Avoid replacing runtime checks with unit-only AST checks. Confirm dataclasses, TreeMap/DynArray, event policy, ABI annotations, default method arguments, nondet API, timestamp semantics and `@gl.contract_interface` are supported by the stable deployed runtime.
5. Inspect architecture critically. Preserve semantics unless there is a proven runtime/security defect; document each necessary change and why it is safe.

## CONSENSUS / SOURCE EVIDENCE — critical

6. `gl.nondet.web.get` and `gl.nondet.exec_prompt` must execute **inside** nondeterministic leader/validator functions. The validator must **independently refetch BOTH** source URLs and **independently rerun** each qualitative invariant assessment. A validator that merely checks the leader's JSON/enums is invalid.
7. Each decisive `PRESERVED`/`VIOLATED` result must be grounded in **both** independently fetched source descriptions. Rejection due to missing facts must not pretend to be conclusive unless backed by a source-grounded standard. Compare exact decision-bearing verdict and source digests, with explicit logic for validator disagreement. Do not let model-generated explanations determine certification.
8. External page content is adversarial input: constrain length, ignore prompt injection, prevent SSRF/source-prefix substitution and URL ambiguity, inspect HTTP status, content changes and redirect behavior. For live examples prefer publicly accessible immutable raw GitHub fixtures pinned to the release commit. Verify that each raw URL is independently retrievable in GenVM and that its content is exactly the pinned fixture.
9. Improve source handling where needed so `UNAVAILABLE` is a real fail-closed first-class outcome and does not inadvertently become certification. Never infer unknown properties as passed. Ensure `AMBIGUOUS`, source failures, malicious leader claims, forged quotes, wrong document digests and malformed LLM JSON are safely handled.
10. Reject mixing findings from two different versions of an originally mutable source. Verify the content-digest consistency check with dedicated tests, including content mutating between two assessments.
11. Ensure semantic decisions remain bound to **role purpose and invariant text** and are explicitly directional. Distinguish functional substitutability from equality or identity. Test `A→B` success while `B→A` remains unauthorized even if both descriptions are similar.

## DETERMINISTIC PROTOCOL / SECURITY REVIEW

12. Examine every role and proposal transition: creation, controlled additions, sealing, candidate submission, per-invariant classification, finalization, certificate query, successor role sealing and expiry. Preserve historical append-only findings/certificate data, but invalidate old authorization in the view.
13. Assert group rules at boundaries: ungrouped required, ALL and ANY, mixed VIOLATED/AMBIGUOUS, all failed ANY group, single satisfied alternative, optional-only failures, and absolute PROHIBITION veto. There must be no implicit acceptance from empty/partially evaluated groups.
14. Audit access control, role successor ownership, multiple unsealed successors, duplicate IDs, cross-role assessments, key/hash normalization, proposal self-substitution, expiry boundary and TTL manipulation. Test `now == expiry`, malformed 64-hex hashes, replay and certificate mismatch.
15. Verify `SubstitutionGate` calls exactly `is_substitutable(proposal_id, expected_role_hash, expected_certificate_hash, original_key, replacement_key)` using a real GenLayer typed interface. A successful read must guard an actual state change. Tests must prove action-hash replay is rejected, reversed identities are rejected, wrong role/certificate hashes are rejected, and superseded/expired certificates stop executing new actions.
16. Keep the implementation self-contained: no frontend, no unnecessary package/web-server, no unsafe secret-handling, no fake deploy reports.

## TESTS — require adversarial evidence

17. Preserve current unit tests and existing Direct Mode scenarios; extend them substantially. Include *working* real Direct Mode tests for every critical state transition and invariant, mocked source fetches, actual `direct_vm.run_validator()` positive consensus and negative forged-leader disagreement where framework supports it, and cross-contract typed-consumer invocation. A static AST check alone does not prove IC-to-IC runtime behavior.
18. Add direct tests for injection in original/replacement sources; forged grounded/unfounded quotes; malformed JSON and extra fields; changing original/replacement source hashes; same URL; source prefix attacks; different domain; document unavailable/oversized/non-200; optional failure; ALL/ANY; prohibition veto; role upgrade; duplicate candidate assessment; late finalization; expiration; stale/incorrect hashes; inverse substitution and one-time consumer action replay.
19. Run test results with actual command/output capture and report counts precisely. If validator disagreement cannot be simulated, explain the exact runtime limitation and use a supported alternative. Never mark a test passing without running it.

## GITHUB + IMMUTABLE PUBLIC FIXTURES

20. After the first real Git commit containing `fixtures/` is pushed to `BeatyXO/SubstituteX`, capture the actual **full 40-character SHA** of that push. **Do not invent it.** Run:

```bash
python scripts/pin_fixture_commit.py <ACTUAL_FULL_40_CHARACTER_COMMIT_SHA>
```

21. Confirm `deployments/fixture_pin.json` points to GitHub raw URLs on THAT SHA, not `main`, not a moving branch, and verify all fixture fetches. Commit/push the pinned manifest and any integration-test updates. Do not leave mocked example SHAs in live tests or deployment docs. The literal dummy URL in Direct Mode tests is not a verified live fixture.
22. Keep the repository default `main` and use ordinary commits and non-force pushes. Verify release SHA and final GitHub files after push.

## REQUIRED LIVE STABLE STUDIONET PROOF

23. Only after Direct Mode passes, deploy the actual `SubstituteX` IC on stable Studionet (chain ID 61999); record real contract address and deploy transaction ID.
24. Execute the positive lifecycle on finalized consensus transactions:
   - create role; add frozen allowed source prefix and 3–5 invariants spanning REQUIRED, OPTIONAL and PROHIBITION (including one real group); seal;
   - capture a real nonempty 64-hex `definition_hash`;
   - create directed candidate proposal with **immutable** public fixture URLs;
   - classify *each* invariant through independently verified consensus;
   - show `get_composition` is derived from these findings;
   - finalize `CERTIFIED` only when the deterministic policy is satisfied;
   - capture a real nonempty 64-hex `certificate_hash`;
   - demonstrate wrong role-hash, wrong certificate-hash and reversed-direction queries returning false.
25. Execute at least one truly negative case (mandatory failure, a prohibition violation, or an unresolved mandatory invariant) where `CERTIFIED` is impossible. Show missing-source `UNAVAILABLE` behavior if stable source-fetch tooling supports a reliable fixture.
26. Deploy **SubstitutionGate** with the finalized SubstituteX address, invoke a protected action with exact pinned data, confirm on-chain state changes, then demonstrate rejected action replay and rejected hash/identity substitution. Also demonstrate that sealing a new role successor prevents a **new** gate action from using an old certificate (historical assessment unchanged). For expiry, use naturally observable time or deterministic Direct Mode time-warp; do not pretend you waited live if you didn't.
27. Verify transaction finality for recorded positive writes. For negative writes, preserve authentic rejection status/receipt/log/trace rather than fabricating a transaction ID. Check on the actual Studionet explorer. If the network is unavailable or live proof is blocked, leave status **BLOCKED / INCOMPLETE** and state why, rather than claiming readiness.

## DOCUMENTATION AND FINAL RELEASE GATES

28. Update `README.md`, `SUBMISSION.md`, `DEPLOYMENT.md`, `BUILD_STATUS.md`, `docs/` and `deployments/studionet.json` to reflect only what actually happened. Record addresses, chain ID, correct RPC, transaction hashes, timestamps, role ID, role hash, proposal ID, finding transaction IDs, final certificate hash, consumer address, successful gated action, failed/replayed action proof, exact test commands/results, known limitations and final Git commit SHA.
29. Add CLI or Python helper scripts for repeatable stable Studionet deployment/lifecycle if the installed tooling warrants it. Verify actual syntax instead of assuming example commands work. Do not fabricate results from fixtures/mocks.
30. Run `python scripts/preflight.py --final`; Python compilation; offline unit tests; every Direct Mode test; intended live integration; and a tracked-file/secret scan (`git status`, `git diff --check`, `git ls-files`). No `.env`, secrets, credentials, venvs, caches, generated artifacts or unrelated files can be committed. No frontend.
31. Confirm only `studionet` / chain ID **61999** is used for live proof. Audit live deployment records and final GitHub repository. Push final release to `https://github.com/BeatyXO/SubstituteX.git` (if local access is authorized) and confirm the public remote contains those exact files.

## FINAL RESPONSE REQUIRED

At the end, report: what files changed; important protocol fixes; exact unit/Direct Mode/integration test results; final `SubstituteX` and `SubstitutionGate` addresses **only if really deployed**; explorer URLs and transaction evidence; full fixture pinned SHA; final Git commit SHA and branch; whether the push actually succeeded; verified network chain ID; and every remaining gap. **Do not claim completion until all applicable verification gates actually pass.** If something remains blocked, clearly identify which gate and why.
