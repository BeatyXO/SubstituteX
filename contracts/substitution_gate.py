# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""Real consumer of SubstituteX's current, role-scoped certification.

An action can only execute once with exact role/certificate/identity pinning.
"""
from genlayer import *
from dataclasses import dataclass


def valid_hash(value: str) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


@gl.contract_interface
class ISubstituteX:
    class View:
        def is_substitutable(self, proposal_id: u256, expected_role_hash: str,
                             expected_certificate_hash: str, original_key: str,
                             replacement_key: str) -> bool: ...
    class Write:
        pass


@allow_storage
@dataclass
class ReplacementUse:
    actor: Address
    proposal_id: u256
    role_hash: str
    certificate_hash: str
    original_key: str
    replacement_key: str
    payload_hash: str


class SubstitutionGate(gl.Contract):
    substitutex_address: Address
    uses: TreeMap[str, ReplacementUse]
    use_count: u256

    def __init__(self, substitutex_address: Address):
        self.substitutex_address = substitutex_address
        self.use_count = u256(0)

    @gl.public.write
    def execute_replacement(self, proposal_id: u256, expected_role_hash: str,
                            expected_certificate_hash: str, original_key: str,
                            replacement_key: str, action_hash: str, payload_hash: str) -> None:
        if not all(valid_hash(s) for s in (expected_role_hash, expected_certificate_hash, action_hash, payload_hash)):
            raise gl.vm.UserError("EXPECTED: hashes must be lowercase 64-hex digests")
        if not original_key or not replacement_key or original_key == replacement_key:
            raise gl.vm.UserError("EXPECTED: invalid substitution identities")
        if action_hash in self.uses:
            raise gl.vm.UserError("EXPECTED: replacement action replay")
        source = ISubstituteX(self.substitutex_address)
        if not source.view().is_substitutable(proposal_id, expected_role_hash, expected_certificate_hash,
                                              original_key, replacement_key):
            raise gl.vm.UserError("EXPECTED: current SubstituteX certificate required")
        self.uses[action_hash] = ReplacementUse(gl.message.sender_address, proposal_id, expected_role_hash,
                                                 expected_certificate_hash, original_key, replacement_key,
                                                 payload_hash)
        self.use_count = u256(int(self.use_count) + 1)

    @gl.public.view
    def was_executed(self, action_hash: str) -> bool:
        return action_hash in self.uses

    @gl.public.view
    def get_execution(self, action_hash: str) -> dict:
        if action_hash not in self.uses:
            raise gl.vm.UserError("EXPECTED: unknown action")
        row = self.uses[action_hash]
        return {"actor": str(row.actor), "proposal_id": int(row.proposal_id), "role_hash": row.role_hash,
                "certificate_hash": row.certificate_hash, "original_key": row.original_key,
                "replacement_key": row.replacement_key, "payload_hash": row.payload_hash}
