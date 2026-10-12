# Studionet integration

Live integration has not been run. Before every live deployment or write, run `genlayer network info` and confirm alias `studionet`, chain ID `61999`, and RPC `https://studio.genlayer.com/api`; then query the RPC's effective chain ID. Do not use preview networks. Pin fixtures only after the initial repository push has returned a real full commit SHA. Record finalized transaction receipts and explorer evidence in `deployments/studionet.json` and `DEPLOYMENT.md`.
