# Reviewer demo: security feed replacement

1. Create role with the purpose `replace the vulnerability feed used by this security monitor`.
2. Add the full immutable GitHub raw **fixture prefix** as a source namespace, then add invariants: CVE IDs required, severity required, ≤24h refresh required, no sale of code prohibited, optional provider metadata.
3. Seal. Record 64-hex definition hash; a post-seal attempt to alter the role must fail.
4. Create proposal `original-provider` → `compatible-provider`, with URL pair and TTL; call `assess_invariant` once per invariant, observing source-grounded model verdicts and validator consensus.
5. Derive certificate through deterministic `finalize_proposal`, confirm directed hash-bounded positive view, negative reversed view, and wrong hash negative view.
6. Create a new role version and seal it; old certificate history still exists but the old `is_substitutable` becomes false.
7. Deploy SubstitutionGate using finalized SubstituteX address and exercise pinned gated action once, wrong role hash rejection, reverse identity rejection, action hash replay rejection, post-supersession rejection. Run on a new valid proposal after invalidating old role if ordering requires.
8. Negative cases: `replacement_bad` yields invariant VIOLATED; `replacement_unknown` yields AMBIGUOUS; missing source yields UNAVAILABLE. None must certify.

The three sample replacement pages are fictional demonstration evidence, not real vendor claims. Pin them to a *real* commit SHA only after public upload and verify their raw URLs from the execution environment.
