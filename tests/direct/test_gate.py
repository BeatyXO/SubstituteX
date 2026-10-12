"""Gate source/interface baseline tests; expand into live cross-contract tests."""
import ast
from pathlib import Path
from gltest.direct import create_address

def test_gate_does_real_typed_contract_read_and_replay_tracking():
    source = (Path(__file__).resolve().parents[2] / "contracts" / "substitution_gate.py").read_text()
    tree = ast.parse(source)
    assert any(isinstance(n, ast.ClassDef) and n.name == "ISubstituteX" for n in tree.body)
    assert "source.view().is_substitutable(" in source
    assert "action_hash in self.uses" in source
    assert "self.uses[action_hash] = ReplacementUse(" in source


def test_gate_executes_through_typed_cross_contract_view(direct_vm, direct_deploy):
    direct_vm.sender = create_address("alice")
    source_address = create_address("substitute-x")
    from gltest.direct.sdk_loader import setup_sdk_paths
    setup_sdk_paths(Path("contracts/substitution_gate.py").resolve(), "v0.2.12")
    from genlayer.py.types import Address
    source_address = Address(source_address)
    gate = direct_deploy("contracts/substitution_gate.py", source_address, sdk_version="v0.2.12")
    role_hash, certificate_hash = "1" * 64, "2" * 64
    calls = []
    source_current = {"allowed": True}

    def route(vm, request):
        call = request.get("CallContract")
        if call is None:
            return None
        calls.append(call)
        assert call["address"].as_bytes == source_address.as_bytes
        args = call["calldata"]["args"]
        assert len(args) == 5
        from genlayer.py import calldata
        from genlayer.py.public_abi import ResultCode
        allowed = source_current["allowed"] and args == [7, role_hash, certificate_hash, "origin-v1", "replacement-v2"]
        return bytes([int(ResultCode.RETURN)]) + calldata.encode(allowed)

    direct_vm._gl_call_hook = route
    gate.execute_replacement(7, role_hash, certificate_hash, "origin-v1", "replacement-v2",
                             "a" * 64, "b" * 64)
    assert gate.was_executed("a" * 64)
    assert gate.get_execution("a" * 64)["payload_hash"] == "b" * 64
    assert calls[-1]["calldata"]["method"] == "is_substitutable"
    with direct_vm.expect_revert("replay"):
        gate.execute_replacement(7, role_hash, certificate_hash, "origin-v1", "replacement-v2",
                                 "a" * 64, "b" * 64)
    with direct_vm.expect_revert("current SubstituteX certificate"):
        gate.execute_replacement(7, "3" * 64, certificate_hash, "origin-v1", "replacement-v2",
                                 "c" * 64, "b" * 64)
    with direct_vm.expect_revert("current SubstituteX certificate"):
        gate.execute_replacement(7, role_hash, "9" * 64, "origin-v1", "replacement-v2",
                                 "f" * 64, "b" * 64)
    with direct_vm.expect_revert("current SubstituteX certificate"):
        gate.execute_replacement(7, role_hash, certificate_hash, "replacement-v2", "origin-v1",
                                 "d" * 64, "b" * 64)
    with direct_vm.expect_revert("lowercase 64-hex"):
        gate.execute_replacement(7, "G" * 64, certificate_hash, "origin-v1", "replacement-v2",
                                 "e" * 64, "b" * 64)
    source_current["allowed"] = False  # Models expiry or successor invalidation in the source view.
    with direct_vm.expect_revert("current SubstituteX certificate"):
        gate.execute_replacement(7, role_hash, certificate_hash, "origin-v1", "replacement-v2",
                                 "9" * 64, "b" * 64)
