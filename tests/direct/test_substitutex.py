"""Direct Mode contract-level adversarial scenarios.

Requires genlayer-test and its matching stable SDK. No assertions are marked
xfail/skip merely to manufacture a passing run.
"""
import json
import pytest
from gltest.direct import create_address

SOURCE = "contracts/substitutex.py"
BASE = "2026-10-12T10:00:00+00:00"
LATER = "2026-10-12T11:00:00+00:00"
FUTURE = "2027-01-01T10:00:00+00:00"
PREFIX = "https://raw.githubusercontent.com/BeatyXO/SubstituteX/0123456789abcdef0123456789abcdef01234567/fixtures/"
ORIGINAL = PREFIX + "original_provider.txt"
REPLACEMENT = PREFIX + "replacement_good.txt"
A_TEXT = ("Original service reports vulnerability identifiers as standard CVE IDs. "
          "Original service publishes a severity rating for every vulnerability. "
          "Original service refreshes its vulnerability feed every twelve hours. ")
B_TEXT = ("Replacement service includes standard CVE identifiers on every finding. "
          "Replacement service publishes numerical severity ratings for every finding. "
          "Replacement service updates its vulnerability feed twice each day. ")


def deploy(vm, factory):
    vm.warp(BASE)
    vm.sender = create_address("alice")
    # Both contract headers pin the stable py-genlayer artifact below. Pinning
    # here prevents the test plugin from selecting a cached preview runtime.
    return factory(SOURCE, sdk_version="v0.2.12")


def create_role(c, prefix=PREFIX):
    r = c.create_role("Vulnerability-feed substitute", "Replace one provider for a security intelligence role.")
    c.add_source_prefix(r, prefix)
    i = c.add_invariant(r, "CVE IDs", "Supply machine-readable standard CVE IDs", 1)
    role_hash = c.seal_role(r)
    return r, i, role_hash


def propose(c, r, ttl=7200):
    return c.propose_substitute(r, "origin-v1", "replacement-v2", ORIGINAL, REPLACEMENT, ttl)


def mock_success(vm):
    vm.mock_web(r"original_provider\.txt", {"status": 200, "body": A_TEXT})
    vm.mock_web(r"replacement_good\.txt", {"status": 200, "body": B_TEXT})
    vm.mock_llm(r"SUBSTITUTEX / ROLE-SCOPED INVARIANT ASSESSMENT", json.dumps({
        "verdict": 1,
        "original_quote": "Original service reports vulnerability identifiers as standard CVE IDs.",
        "replacement_quote": "Replacement service includes standard CVE identifiers on every finding."
    }))


def test_role_seal_definition_hash_and_mutation_lock(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r, _, role_hash = create_role(c)
    assert len(role_hash) == 64
    assert c.get_role(r)["status"] == 2
    with direct_vm.expect_revert("role not owned/open"):
        c.add_invariant(r, "other", "extra requirement", 1)


def test_authorship_and_unsealed_role_rejected(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r = c.create_role("Role", "Purpose")
    with direct_vm.prank(create_address("bob")):
        with direct_vm.expect_revert("role not owned/open"):
            c.add_source_prefix(r, PREFIX)
    with direct_vm.expect_revert("must propose for current sealed role"):
        propose(c, r)


def test_source_prefix_is_frozen_and_cannot_be_bypassed(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r, _, _ = create_role(c)
    with direct_vm.expect_revert("source outside sealed namespace"):
        c.propose_substitute(r, "old", "new", "https://attacker.example/claims", REPLACEMENT, 1000)


def test_cannot_self_substitute(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r, _, _ = create_role(c)
    with direct_vm.expect_revert("distinct identities"):
        c.propose_substitute(r, "same", "same", ORIGINAL, REPLACEMENT, 1000)


def test_real_consensus_source_grounded_assessment_and_certificate(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r, i, role_hash = create_role(c)
    p = propose(c, r)
    mock_success(direct_vm)
    assert c.assess_invariant(p, i) == 1
    assert direct_vm.run_validator() is True
    with direct_vm.expect_revert("already assessed"):
        c.assess_invariant(p, i)
    assert c.get_composition(p)["certifiable"] is True
    assert c.finalize_proposal(p) == 4
    row = c.get_proposal(p)
    assert len(row["certificate_hash"]) == 64
    assert c.is_substitutable(p, role_hash, row["certificate_hash"], "origin-v1", "replacement-v2")
    assert not c.is_substitutable(p, "f"*64, row["certificate_hash"], "origin-v1", "replacement-v2")
    assert not c.is_substitutable(p, role_hash, row["certificate_hash"], "replacement-v2", "origin-v1")


def test_validator_rejects_forged_leader_verdict(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r, i, _ = create_role(c)
    p = propose(c, r)
    mock_success(direct_vm)
    c.assess_invariant(p, i)
    forged = {
        "verdict": 2,
        "original_quote": "Original service reports vulnerability identifiers as standard CVE IDs.",
        "replacement_quote": "Replacement service includes standard CVE identifiers on every finding.",
        "original_digest": "0" * 64,
        "replacement_digest": "0" * 64,
    }
    assert direct_vm.run_validator(leader_result=forged) is False


def test_source_digest_change_between_findings_fails_closed(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r = c.create_role("Snapshot test", "Keep both source snapshots stable across findings.")
    c.add_source_prefix(r, PREFIX)
    first = c.add_invariant(r, "First", "First required check", 1)
    second = c.add_invariant(r, "Second", "Second required check", 1)
    c.seal_role(r)
    p = propose(c, r)
    ambiguous = json.dumps({"verdict": 3, "original_quote": "", "replacement_quote": ""})
    direct_vm.mock_web(r"original_provider\.txt", {"status": 200, "body": A_TEXT})
    direct_vm.mock_web(r"replacement_good\.txt", {"status": 200, "body": B_TEXT})
    direct_vm.mock_llm(r"SUBSTITUTEX / ROLE-SCOPED INVARIANT ASSESSMENT", ambiguous)
    c.assess_invariant(p, first)
    direct_vm.clear_mocks()
    direct_vm.mock_web(r"original_provider\.txt", {"status": 200, "body": A_TEXT + "Updated snapshot."})
    direct_vm.mock_web(r"replacement_good\.txt", {"status": 200, "body": B_TEXT})
    direct_vm.mock_llm(r"SUBSTITUTEX / ROLE-SCOPED INVARIANT ASSESSMENT", ambiguous)
    with direct_vm.expect_revert("source snapshot changed"):
        c.assess_invariant(p, second)


def test_violated_required_invariant_blocks_certification(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r, i, role_hash = create_role(c)
    p = propose(c, r)
    direct_vm.mock_web(r"original_provider\.txt", {"status": 200, "body": A_TEXT})
    direct_vm.mock_web(r"replacement_good\.txt", {"status": 200, "body": B_TEXT})
    direct_vm.mock_llm(r"SUBSTITUTEX / ROLE-SCOPED INVARIANT ASSESSMENT", json.dumps({
        "verdict": 2,
        "original_quote": "Original service reports vulnerability identifiers as standard CVE IDs.",
        "replacement_quote": "Replacement service includes standard CVE identifiers on every finding."
    }))
    c.assess_invariant(p, i)
    assert c.get_composition(p)["failed"] == 1
    assert c.finalize_proposal(p) == 3
    assert not c.is_substitutable(p, role_hash, "f"*64, "origin-v1", "replacement-v2")


def test_ambiguous_assessment_blocks_certification(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r, i, _ = create_role(c)
    p = propose(c, r)
    direct_vm.mock_web(r"original_provider\.txt", {"status": 200, "body": A_TEXT})
    direct_vm.mock_web(r"replacement_good\.txt", {"status": 200, "body": B_TEXT})
    direct_vm.mock_llm(r"SUBSTITUTEX / ROLE-SCOPED INVARIANT ASSESSMENT", json.dumps({
        "verdict": 3, "original_quote": "", "replacement_quote": ""
    }))
    c.assess_invariant(p, i)
    assert c.get_composition(p)["unresolved"] == 1
    assert c.finalize_proposal(p) == 3


@pytest.mark.parametrize("bad_response", [
    {"status": 503, "body": "temporarily unavailable"},
    {"status": 200, "body": "x" * 14001},
])
def test_unavailable_and_oversized_sources_fail_closed(direct_vm, direct_deploy, bad_response):
    c = deploy(direct_vm, direct_deploy)
    r, i, _ = create_role(c)
    p = propose(c, r)
    direct_vm.mock_web(r"original_provider\.txt", {"status": 200, "body": A_TEXT})
    direct_vm.mock_web(r"replacement_good\.txt", bad_response)
    assert c.assess_invariant(p, i) == 4
    finding = c.get_finding(p, i)
    assert finding["verdict"] == 4
    assert finding["original_quote"] == finding["replacement_quote"] == ""
    assert c.finalize_proposal(p) == 3


def test_optional_failure_does_not_veto_any_group_success(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r = c.create_role("Grouped policy", "Meet the role's functional requirements.")
    c.add_source_prefix(r, PREFIX)
    required = c.add_invariant(r, "Required", "Required baseline", 1)
    any_failed = c.add_invariant(r, "Alternative one", "Alternative path one", 1, 1, 2)
    any_passed = c.add_invariant(r, "Alternative two", "Alternative path two", 1, 1, 2)
    optional = c.add_invariant(r, "Optional", "Optional metadata", 2)
    prohibition = c.add_invariant(r, "No resale", "Do not resell customer code", 3)
    c.seal_role(r)
    p = propose(c, r)
    direct_vm.mock_web(r"original_provider\.txt", {"status": 200, "body": A_TEXT})
    direct_vm.mock_web(r"replacement_good\.txt", {"status": 200, "body": B_TEXT})
    passed = {"verdict": 1,
              "original_quote": "Original service reports vulnerability identifiers as standard CVE IDs.",
              "replacement_quote": "Replacement service includes standard CVE identifiers on every finding."}
    failed = {"verdict": 2,
              "original_quote": "Original service reports vulnerability identifiers as standard CVE IDs.",
              "replacement_quote": "Replacement service includes standard CVE identifiers on every finding."}
    for invariant, verdict in ((required, passed), (any_failed, failed), (any_passed, passed),
                               (optional, failed), (prohibition, passed)):
        direct_vm.mock_llm("REQUIREMENT: " + c.get_invariant(invariant)["requirement"], json.dumps(verdict))
        c.assess_invariant(p, invariant)
    composition = c.get_composition(p)
    assert composition["failed"] == 0
    assert composition["unresolved"] == 0
    assert composition["optional_not_preserved"] == 1
    assert composition["certifiable"] is True
    assert c.finalize_proposal(p) == 4


def test_prohibition_violation_is_absolute_veto(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r = c.create_role("Prohibition", "Do not expose customer code.")
    c.add_source_prefix(r, PREFIX)
    required = c.add_invariant(r, "CVE IDs", "Supply standard CVE IDs", 1)
    prohibition = c.add_invariant(r, "No resale", "Do not resell customer code", 3)
    c.seal_role(r)
    p = propose(c, r)
    direct_vm.mock_web(r"original_provider\.txt", {"status": 200, "body": A_TEXT})
    direct_vm.mock_web(r"replacement_good\.txt", {"status": 200, "body": B_TEXT})
    passed = {"verdict": 1,
              "original_quote": "Original service reports vulnerability identifiers as standard CVE IDs.",
              "replacement_quote": "Replacement service includes standard CVE identifiers on every finding."}
    violated = dict(passed, verdict=2)
    for invariant, verdict in ((required, passed), (prohibition, violated)):
        direct_vm.mock_llm("REQUIREMENT: " + c.get_invariant(invariant)["requirement"], json.dumps(verdict))
        c.assess_invariant(p, invariant)
    assert c.get_composition(p)["failed"] == 1
    assert c.finalize_proposal(p) == 3


def test_cannot_finalize_incomplete_candidate(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r, _, _ = create_role(c)
    p = propose(c, r)
    with direct_vm.expect_revert("incomplete invariant assessments"):
        c.finalize_proposal(p)


def test_expiry_blocks_assessment(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r, i, _ = create_role(c)
    p = propose(c, r, ttl=5)
    direct_vm.warp(LATER)
    with direct_vm.expect_revert("no longer assessable"):
        c.assess_invariant(p, i)


def test_expiry_is_closed_at_exact_boundary(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r, i, _ = create_role(c)
    p = propose(c, r, ttl=5)
    direct_vm.warp("2026-10-12T10:00:05+00:00")
    with direct_vm.expect_revert("no longer assessable"):
        c.assess_invariant(p, i)


def test_supersession_invalidates_old_certificate_without_rewriting_it(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r, i, role_hash = create_role(c)
    p = propose(c, r)
    mock_success(direct_vm)
    c.assess_invariant(p, i)
    c.finalize_proposal(p)
    cert = c.get_proposal(p)["certificate_hash"]
    next_role = c.create_role("Vulnerability-feed substitute v2", "Different scope of service", r)
    c.add_source_prefix(next_role, PREFIX)
    c.add_invariant(next_role, "Freshness", "Must update every twelve hours", 1)
    c.seal_role(next_role)
    assert c.get_role(r)["successor_id"] == next_role
    assert c.get_proposal(p)["certificate_hash"] == cert
    assert c.is_substitutable(p, role_hash, cert, "origin-v1", "replacement-v2") is False


def test_mixed_group_semantics_are_declared_not_model_chosen(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    r = c.create_role("Group test", "Cover requirement by alternate means")
    c.add_source_prefix(r, PREFIX)
    a = c.add_invariant(r, "Path A", "First acceptable interoperability mechanism", 1, 1, 2)
    b = c.add_invariant(r, "Path B", "Second acceptable interoperability mechanism", 1, 1, 2)
    c.seal_role(r)
    assert c.get_invariant(a)["group_rule"] == 2
    assert c.get_invariant(b)["group_rule"] == 2
    with direct_vm.expect_revert("role not owned/open"):
        c.add_invariant(r, "New A", "Late changed rule", 1)
