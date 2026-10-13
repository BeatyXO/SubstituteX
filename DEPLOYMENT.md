# Stable Studionet deployment and lifecycle evidence

**Status: live deployments and protocol lifecycle verified on stable Studionet.** The current record is `deployments/studionet.json`; the human-readable transaction links below point to the required explorer.

## Network lock and fixture evidence

The GenLayer CLI `0.39.1` reported `studionet`, chain ID `61999`, and RPC `https://studio.genlayer.com/api`. A direct JSON-RPC `eth_chainId` check returned `0xf22f`. These checks were repeated immediately before each deploy and each state-changing lifecycle write. No preview network was used. The explorer used for inspection is [explorer-studio.genlayer.com](https://explorer-studio.genlayer.com).

The fixture source prefix is `https://raw.githubusercontent.com/BeatyXO/SubstituteX/246a12ceb2ae1a8b4b643b99a5153868fff99c43/fixtures/`. The four original/good/bad/unknown fixture URLs returned HTTP 200 and their response contents matched the committed files. This is the initial pushed fixture commit; the pin manifest itself is committed separately.

## Deployments

| Contract | Address | Deployment transaction |
| --- | --- | --- |
| SubstituteX | `0x49e6192080F04cD22B5EEB49847254246A9b697A` | [Finalized receipt](https://explorer-studio.genlayer.com/tx/0xf12f48d98dadabc2a7b0739d3c897d916add48bff646d5c68d120d51b91fc0d1) |
| SubstitutionGate | `0x8Fd67e5149e1B02Ed9A6329Bca14765502995cE5` | [Finalized receipt](https://explorer-studio.genlayer.com/tx/0x6d85b5f231673cf307f5f1619106fe570e9e32e7ad411b32103044e1027d25fc) |

Both deploy receipts reached `FINALIZED`, with successful GenVM execution and majority agreement.

## Positive proposal

Role 1 (`SubstituteX live demo`) is version 1, owned by the deployment account, and sealed with definition hash `b5bc6970094b75ac3d927e48363fed231ef2b2b8340327946965ec3d03abb4df`. Its five invariants cover a required CVE identifier, an `ANY` group for daily/twelve-hour feed freshness, optional remediation guidance, and a source-code confidentiality prohibition. The role prefix and every proposal URL use the pinned fixture commit.

Proposal 1 binds `provider:original → provider:replacement-good`, the sealed role hash, the pinned original and good replacement pages, and an expiry. All five findings store the same original digest `55d49568ac7f9593e15ac7209078d382affaf12eb3345fcf8ace97644f78b922` and replacement digest `5e3cb09f021c49c99d9b8837056ee1f93276fe6787be8e7f6be6e26a0f8fd938`. Verdicts were `[PRESERVED, PRESERVED, PRESERVED, UNAVAILABLE, PRESERVED]`. The `UNAVAILABLE` optional finding was counted in `optional_not_preserved` and did not silently become a pass.

`get_composition(1)` returned `evaluated=5`, `failed=0`, `unresolved=0`, `optional_not_preserved=1`, `certifiable=true`. Deterministic finalization transaction [0x33738a8a…d2e5d5a](https://explorer-studio.genlayer.com/tx/0x33738a8a8d67046ffff91b9e2d493ebbdc784e6d56aae03be42b625d8d2e5d5a) succeeded and returned `CERTIFIED` (4). The certificate hash is `229fed246ee71c33c596695f883a8834151c42061466531d47da738f4131e052`.

The live query returned `true` only for the exact role hash, certificate hash, original key and replacement key. Wrong role hash, wrong certificate hash, and reversed identity queries each returned `false`.

## Negative proposal

Proposal 2 uses the pinned bad replacement fixture. Its five finalized assessments returned `VIOLATED` for the CVE requirement, both freshness alternatives, the optional remediation invariant, and the source-code confidentiality prohibition. `get_composition(2)` returned `evaluated=5`, `failed=3`, `unresolved=0`, `optional_not_preserved=1`, `certifiable=false`. Finalization transaction `0x9fd07a755689ce250ef7435b3712ed26b9d2e458d4b2de95ecca806294883cc2` finalized as `REJECTED` (3) and the proposal has an empty certificate hash.

There was one earlier finalized `MAJORITY_DISAGREE` assessment attempt, transaction `0x888def1d859c0a6c4fcf48368ee19ff09d7515a024e709f575fe7711335936d3`, with three validator disagreement votes and one agreement. It did not store a finding; the proposal's evaluated count remained unchanged. The retry finalized with majority agreement. This is a live fail-closed example, not a fabricated finding.

## Typed consumer and successor invalidation

SubstitutionGate was deployed with the SubstituteX address and uses the typed `ISubstituteX` view interface. The successful [execute_replacement receipt](https://explorer-studio.genlayer.com/tx/0xd298c28b457eb5a964817f994d20ce87c4e0d942a507979261dd8c18765f3f1a) is finalized, accepted, and has successful GenVM execution. Its state records action hash `6f3d358dea56b8deea256b050fdcd7a0fd521559f97d0b19b9bf56c8d71130dd`, payload hash `013d227caa156e2d71ea0276be14c847e16a1cbb62f1f205b87e18f487c4e49f`, and the exact proposal, role, certificate, and identity keys.

The [replayed action receipt](https://explorer-studio.genlayer.com/tx/0x42422df6b90ae68a2832d74deb9dc8299954fbe541d17c8957a3fb9874cea3c8) finalized with a GenVM rollback and `EXPECTED: replacement action replay`. A well-formed wrong certificate hash and reversed identity pair each finalized with `EXPECTED: current SubstituteX certificate required` (transactions `0x93c29c1a32c7614a2e7d1e615d8e18a3861f46285127e740f6d2f5ec6e73d0c4` and `0x8959f1f5ecf09b8ee444f52d635063e47177c63b1ca0b5f062ab7d1a0b57f006`). An all-numeric 64-character value was parsed as an integer by the CLI and separately rejected by hash-format validation; that transaction is not counted as the well-formed hash test.

Successor role 2 (version 2) was created with `previous_role_id=1`, given the same invariant policy and sealed with hash `2619662669841a421e85af8894de0027ea9bbc74374848c74a64f6e2df98bc27`. Role 1 now reports `successor_id=2`. Proposal 1 remains historically `CERTIFIED`, but `is_substitutable` returns `false`, and a new Gate action with its old certificate finalized as rejected in `0xdb341f437b574e8082fc9aa40db3ff388ecfd8b0612ac971138f18b45d76c3b2`.

## Evidence limits

- Direct Mode time-warp tests cover `now == expiry`; no live expiry wait is claimed.
- Stable RPC intermittently returned an HTML gateway response in place of JSON. Where a transaction hash had already been returned, the receipt was fetched later and no blind resubmission occurred.
- The CLI trace command called `gen_dbg_traceTransaction`, which stable Studionet reported as unavailable. Finalized receipts and the rendered explorer pages were used for transaction status and execution results.
- The explorer rendered the SubstituteX deployment, successful certification, successful Gate action and replay rollback. Full transaction IDs and all write receipts remain in `deployments/studionet.json`.
