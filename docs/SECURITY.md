# Threat model

**Malicious fixture/document:** treat source bytes as data only, bound length (14 kB) and HTML-aware evaluation. Ensure model does not follow instructions embedded in the source; fuzz injection attacks in both documents. Real production deployments should only accept trusted content authorities, with narrow immutable URL prefixes.

**Source swapping or SSRF:** HTTPS only, path-scoped sealed namespace, reject ambiguous URI components, local and numeric hosts, and enforce source membership when proposing. Audit web redirects and resolved IP behavior during runtime verification; if web fetch redirects outside the prefix, use immutable GitHub raw URLs or reject and document unsupported cases. Public source hosts are not synonymous with truthful authorities.

**Leader forgery:** validator fetches both sources independently and re-evaluates the requirement, checks both source hashes, and independently checks leader quotes. `PRESERVED`/`VIOLATED` fail without exact grounded evidence on both sides. Detect malformed responses, divergent validators and unavailable pages.

**Inadequate counterevidence:** a quote can be genuine but non-decisive, or a source may hide omitted facts. The classifier is a consensus-backed bounded judgment, not mathematical proof of all real-world properties. For high-stakes substitutes, require pinned canonical source specs, disconfirming evidence, and model uncertainty.

**Role/version replay:** consumer pins definition and certificate hash; old role authorization is revoked on successor seal, but prior historical certificate remains auditable. Concurrent transactions and contract-specific finality must be tested on Studionet.

**Time attacks:** use chain transaction time instead of local wall clock; test Direct Mode warped time, view behavior, near-expiry and post-expiry semantics.

**Denial of service:** bound role counts per invariant and group, page bytes, source-prefix count and TTL. Repeated proposals can still incur proposer-paid costs and storage growth. No monetary escrow or funds are at risk inside primitive.

**Aspirational remaining checks:** deploy and invoke the typed consumer using actual chain ID 61999; validator divergence with forged leader claims and web-fetch errors; prompt-injection fixtures; onchain action replay; stable CLI fee estimation. Do not mark as verified until live evidence exists.

## Local runtime evidence

The 21 passing Direct Mode scenarios include forged leader disagreement, changed source snapshots between findings, expiry at the exact boundary, optional failure with a satisfied `ANY` group, prohibition veto, and unavailable or oversized source responses. The typed gate test uses GenLayer Test's Direct Mode `CallContract` hook. Real RPC source fetching and a finalized onchain consumer call remain unverified because the initial repository push was denied.
