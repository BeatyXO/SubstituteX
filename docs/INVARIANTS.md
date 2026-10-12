# Reviewable invariants

1. No unsealed role can accept a proposal.
2. Only the creator of an OPEN role can add source prefixes or invariants; after sealing neither changes.
3. Source URL must match a frozen, path-scoped HTTPS prefix and may not contain encoding, traversal, userinfo or query/fragment ambiguity.
4. Substitution is directed and requires two distinct keys and two distinct URLs; reverse direction does not inherit certification.
5. Every proposal pins role definition hash and evaluation source URLs at admission.
6. Each role invariant is evaluated at most once per proposal; each assessment is bound to both independently fetched source digests. Digests must remain consistent across all invariant assessments in one proposal.
7. Decisive leader outcomes require independently checked, verbatim source quotes in both source documents.
8. Validator independently re-fetches and re-evaluates each invariant; schema validation alone is not consensus.
9. All REQUIRED group semantics and PROHIBITION vetoes are deterministic, predeclared and immutable.
10. OPTIONAL failure is visible but does not veto; missing/incomplete mandatory assessments cannot be certified.
11. Any mandatory AMBIGUOUS/UNAVAILABLE result blocks certification; no rounding of uncertainty into PRESERVED.
12. Certificates bind role hash, directed identities, expiry, proposal and all ordered findings.
13. Sealing a successor invalidates historical certificate **authorization** without rewriting historical assessment/certificate.
14. Expired certificates cannot be used in fresh consumer actions; completion is checked at execution time.
15. Typed cross-contract read pins exact role hash, certificate hash, identity direction and proposal ID; gate action hashes cannot replay.
16. No uncontrolled funds movement, no frontend, no invented deployment proof.
