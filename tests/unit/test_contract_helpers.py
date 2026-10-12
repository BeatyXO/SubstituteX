"""Dependency-free tests of the actual helpers extracted from the contract AST."""
import ast
import json
from pathlib import Path
from types import SimpleNamespace
import pytest

SOURCE = Path(__file__).resolve().parents[2] / "contracts" / "substitutex.py"
NAMES = ("fail", "bounded", "safe_url", "safe_prefix", "url_within", "parse_assessment", "assessment_key")

class UserError(Exception):
    pass

@pytest.fixture(scope="module")
def helpers():
    source = ast.parse(SOURCE.read_text())
    funcs = [node for node in source.body if isinstance(node, ast.FunctionDef) and node.name in NAMES]
    module = ast.Module(body=funcs, type_ignores=[])
    ast.fix_missing_locations(module)
    env = {"gl": SimpleNamespace(vm=SimpleNamespace(UserError=UserError)), "json": json,
           "PRESERVED": 1, "VIOLATED": 2, "AMBIGUOUS": 3, "UNAVAILABLE": 4}
    exec(compile(module, str(SOURCE), "exec"), env)
    return env

def test_source_prefix_is_path_scoped(helpers):
    p = "https://raw.githubusercontent.com/BeatyXO/SubstituteX/abc123/fixtures/"
    assert helpers["safe_prefix"](p) == p
    with pytest.raises(UserError):
        helpers["safe_prefix"]("https://raw.githubusercontent.com/")
    assert helpers["url_within"](p + "original.txt", [p])
    assert not helpers["url_within"](p[:-1] + "-evil/file.txt", [p])
    assert not helpers["url_within"]("https://other.org/original.txt", [p])

@pytest.mark.parametrize("url", [
    "http://example.com/path/file", "https://localhost/a/b", "https://x.local/a/b",
    "https://USER@host.example/path", "https://host.example:443/file", "https://host.example/%2f/x",
    "https://host.example/a/../secret", "https://host.example/a//b",
    "https://host.example/file?x=y", "https://host.example/file#x", "https://host.example\\@other/file"
    , "https://host.example/a b", "https://host.example/a\nb", "https://bad_host.example/a/b",
    "https://service.localhost/a/b", "https://host.example./a/b"
])
def test_unsafe_url_rejected(helpers, url):
    with pytest.raises(UserError):
        helpers["safe_url"](url)

def test_decisive_quote_must_be_grounded_in_both_pages(helpers):
    orig = "Original service delivers CVE identifiers in machine-readable records."
    new = "Replacement service delivers standard CVE identifiers in JSON records."
    assessment = {"verdict": 1, "original_quote": "Original service delivers CVE identifiers",
                  "replacement_quote": "Replacement service delivers standard CVE identifiers"}
    assert helpers["parse_assessment"](json.dumps(assessment), orig, new)["verdict"] == 1
    for field in ("original_quote", "replacement_quote"):
        forged = dict(assessment, **{field: "Unrelated forged text not in any source"})
        with pytest.raises(ValueError):
            helpers["parse_assessment"](forged, orig, new)

@pytest.mark.parametrize("bad", ["not JSON", "[]", "{}", "{\"verdict\":true}",
                                '{"verdict": 9, "original_quote":"", "replacement_quote":""}'])
def test_malformed_model_output_fails_closed(helpers, bad):
    with pytest.raises(ValueError):
        helpers["parse_assessment"](bad, "original", "replacement")

def test_undecidable_evidence_is_not_promoted_to_decisive(helpers):
    for result in [3, 4]:
        assert helpers["parse_assessment"]({"verdict": result, "original_quote": "", "replacement_quote": ""}, "a", "b")["verdict"] == result


def test_composite_key_namespaces_proposal_and_invariant(helpers):
    assert helpers["assessment_key"](1, 12) != helpers["assessment_key"](11, 2)


def test_aggregate_all_any_optional_prohibition_logic():
    # Execute the real contract method with a tiny fake storage interface.
    source = ast.parse(SOURCE.read_text())
    cls = next(n for n in source.body if isinstance(n, ast.ClassDef) and n.name == "SubstituteX")
    method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "_aggregate")
    mod = ast.Module(body=[method], type_ignores=[])
    ast.fix_missing_locations(mod)
    ns = {"ALL": 1, "ANY": 2, "REQUIRED": 1, "OPTIONAL": 2, "PROHIBITION": 3,
          "PRESERVED": 1, "VIOLATED": 2, "AMBIGUOUS": 3,
          "assessment_key": lambda pid, iid: f"{pid}:{iid}", "u256": int, "Proposal": object}
    exec(compile(mod, str(SOURCE), "exec"), ns)
    agg = ns["_aggregate"]
    # Group 1 ANY: one violation + one preserved means group is satisfied.
    # Optional failed does not veto. Prohibition preserved avoids veto.
    inv = {1: (1, 1, 2), 2: (1, 1, 2), 3: (2, 0, 1), 4: (3, 0, 1), 5: (1, 0, 1)}
    def run(verdicts, evaluated=5):
        role = SimpleNamespace(invariant_ids=[1, 2, 3, 4, 5])
        me = SimpleNamespace(_role=lambda role_id: role,
            invariants={iid: SimpleNamespace(kind=kind, group_id=gid, group_rule=rule)
                        for iid, (kind, gid, rule) in inv.items()},
            findings={f"1:{iid}": SimpleNamespace(verdict=v) for iid, v in verdicts.items()})
        proposal = SimpleNamespace(role_id=1, evaluated=evaluated)
        return agg(me, 1, proposal)
    assert run({1: 2, 2: 1, 3: 2, 4: 1, 5: 1})[:3] == (0, 0, 1)
    assert run({1: 2, 2: 2, 3: 1, 4: 1, 5: 1})[0] == 1
    assert run({1: 2, 2: 3, 3: 1, 4: 1, 5: 1})[1] == 1
    assert run({1: 1, 2: 2, 3: 1, 4: 2, 5: 1})[0] == 1
    assert run({1: 1, 2: 2, 3: 1, 4: 1, 5: 2})[0] == 1
    assert run({1: 1, 2: 2, 3: 1, 4: 1, 5: 1}, evaluated=4)[1] == 1
