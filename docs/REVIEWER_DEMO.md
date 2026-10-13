# Reviewer demo: security-feed substitution

This is a record of the live stable Studionet demonstration, not a mockup. Full transaction hashes and findings are in [`deployments/studionet.json`](../deployments/studionet.json).

1. SubstituteX was deployed at `0x49e6192080F04cD22B5EEB49847254246A9b697A`; SubstitutionGate was deployed at `0x8Fd67e5149e1B02Ed9A6329Bca14765502995cE5`. Both deploy receipts finalized on chain 61999.
2. Role 1 declared its security-operations purpose, the immutable raw GitHub fixture prefix, a REQUIRED CVE invariant, a two-member REQUIRED `ANY` feed-freshness group, OPTIONAL remediation guidance, and a source-code confidentiality PROHIBITION. Sealing produced `b5bc6970094b75ac3d927e48363fed231ef2b2b8340327946965ec3d03abb4df`.
3. The proposal `provider:original → provider:replacement-good` used two different URLs pinned to the original published fixture commit. Five separate consensus transactions independently assessed the invariants. The source digests stayed consistent; the optional remediation finding was `UNAVAILABLE`.
4. Deterministic composition returned five evaluated, zero failed, zero unresolved, one optional not preserved, and `certifiable=true`. Finalization returned `CERTIFIED`, certificate `229fed246ee71c33c596695f883a8834151c42061466531d47da738f4131e052`. Exact identity/hash query was true; wrong role hash, wrong certificate hash and reversed identities were false.
5. The Gate made a typed view call to SubstituteX and recorded one pinned action in finalized transaction [`0xd298c28b…765f3f1a`](https://explorer-studio.genlayer.com/tx/0xd298c28b457eb5a964817f994d20ce87c4e0d942a507979261dd8c18765f3f1a). Reusing the action hash was rejected with `EXPECTED: replacement action replay` in finalized transaction [`0x42422df6…7cea3c8`](https://explorer-studio.genlayer.com/tx/0x42422df6b90ae68a2832d74deb9dc8299954fbe541d17c8957a3fb9874cea3c8).
6. A second proposal against the pinned bad replacement fixture finalized as `REJECTED`. Its CVE requirement, `ANY` freshness group and confidentiality PROHIBITION failed. The full findings and finalization transaction are recorded in the deployment manifest.
7. Successor role 2 was sealed as version 2. Role 1 now points to role 2; proposal 1 remains historically `CERTIFIED`, while new authorization queries and Gate actions using its old certificate are rejected.

The pages are fictional fixtures for protocol testing and do not make real vendor claims. Exact expiry behavior is covered by local Direct Mode time-warp tests; no live waiting period is claimed.
