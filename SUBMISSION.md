# Submission status

## Product and repository

SubstituteX is a standalone reusable GenLayer Intelligent Contract primitive. It has no frontend, token, escrow, or unrelated application machinery. The repository is published at [BeatyXO/SubstituteX](https://github.com/BeatyXO/SubstituteX) on `main`. The initial fixture commit is `246a12ceb2ae1a8b4b643b99a5153868fff99c43`; all fixture URLs use that immutable SHA and were independently fetched with HTTP 200 and compared against the fixture contents.

## Stable network proof

- Alias: `studionet`
- Chain ID: `61999` (`eth_chainId = 0xf22f`)
- RPC: `https://studio.genlayer.com/api`
- Explorer: [GenLayer Studio Explorer](https://explorer-studio.genlayer.com)

The installed CLI is GenLayer `0.39.1`. The active account was unlocked on Studionet and had sufficient GEN for the requested workflow. Network info and RPC chain ID were checked before every deployment and write submission; `scripts/studionet_write.py` automates those checks for each lifecycle write.

## Live contracts and behavior

- SubstituteX: `0x49e6192080F04cD22B5EEB49847254246A9b697A`, deployed in finalized transaction [`0xf12f48d9…b91fc0d1`](https://explorer-studio.genlayer.com/tx/0xf12f48d98dadabc2a7b0739d3c897d916add48bff646d5c68d120d51b91fc0d1).
- SubstitutionGate: `0x8Fd67e5149e1B02Ed9A6329Bca14765502995cE5`, deployed in finalized transaction [`0x6d85b5f2…7d25fc`](https://explorer-studio.genlayer.com/tx/0x6d85b5f231673cf307f5f1619106fe570e9e32e7ad411b32103044e1027d25fc).
- Role 1 sealed to `b5bc6970094b75ac3d927e48363fed231ef2b2b8340327946965ec3d03abb4df`; proposal 1 to the good fixture was `CERTIFIED` with certificate `229fed246ee71c33c596695f883a8834151c42061466531d47da738f4131e052`.
- Proposal 2 against the bad fixture was `REJECTED`: three failures, zero unresolved findings, and no certificate.
- The Gate's finalized action transaction is [`0xd298c28b…765f3f1a`](https://explorer-studio.genlayer.com/tx/0xd298c28b457eb5a964817f994d20ce87c4e0d942a507979261dd8c18765f3f1a). It recorded the exact role hash, certificate hash and directed identity pair. Replay was rejected in [`0x42422df6…7cea3c8`](https://explorer-studio.genlayer.com/tx/0x42422df6b90ae68a2832d74deb9dc8299954fbe541d17c8957a3fb9874cea3c8). A wrong well-formed certificate and reversed identities were also rejected.
- Sealing successor role 2 invalidated new use of role 1's still-queryable historical certificate. The old-certificate Gate action was rejected in transaction `0xdb341f437b574e8082fc9aa40db3ff388ecfd8b0612ac971138f18b45d76c3b2`.

The full lifecycle transaction list, findings, source digests, certificate hashes, rejection reasons, and explorer links are in [`deployments/studionet.json`](deployments/studionet.json). Exact expiry-boundary behavior was verified by Direct Mode time-warp tests; no claim is made that live time was advanced to expiry.

## Validation

The release gate commands and their final output are recorded in [`BUILD_STATUS.md`](BUILD_STATUS.md). Direct Mode is local runtime evidence; the finalized Gate transaction separately verifies actual on-chain typed cross-contract behavior.

## Remaining limitations

- Stable Studionet's trace RPC method is unavailable, so transaction receipts and explorer detail pages provide the transaction evidence.
- The RPC intermittently returned an HTML gateway response instead of JSON. Affected transaction hashes were retained and receipts checked later before deciding whether a retry was safe.
- There was one finalized validator-disagreement attempt for a freshness assessment; it persisted no finding. The retry reached majority agreement and the stored source digests matched all findings in that proposal.
- The final full 40-character Git commit SHA is reported after pushing and verifying the remote `main` branch. The deployment manifest does not try to embed its own commit's SHA, which would be self-referential.
