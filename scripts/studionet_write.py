#!/usr/bin/env python3
"""Submit one Studionet write only after verifying the configured stable network.

This helper intentionally refuses every network except stable Studionet (61999).
It captures the actual transaction hash and waits for a finalized receipt.
Arguments after METHOD are forwarded as GenLayer CLI --args values.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

RPC = "https://studio.genlayer.com/api"
CHAIN_ID = "61999"


def cli(command: list[str]) -> list[str]:
    """Resolve the npm CLI entrypoint in both POSIX and Windows shells."""
    if os.name == "nt":
        node = shutil.which("node")
        appdata = os.environ.get("APPDATA")
        entry = Path(appdata or "") / "npm" / "node_modules" / "genlayer" / "dist" / "index.js"
        if node and entry.is_file():
            return [node, str(entry), *command]
    return ["genlayer", *command]


def run(command: list[str], timeout: int = 600) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    output = result.stdout + result.stderr
    if result.returncode:
        raise SystemExit(output[-12000:] or f"Command failed: {command[0]}")
    return output


def verify_network() -> None:
    info = run(cli(["network", "info"]), timeout=120)
    if not re.search(r"alias:\s*['\"]studionet['\"]", info):
        raise SystemExit("Refusing write: CLI alias is not studionet")
    if not re.search(r"chainId:\s*['\"]61999['\"]", info):
        raise SystemExit("Refusing write: CLI chain ID is not 61999")
    if RPC not in info:
        raise SystemExit("Refusing write: CLI RPC is not the required stable endpoint")
    if os.name == "nt":
        powershell = shutil.which("powershell") or shutil.which("pwsh")
        if not powershell:
            raise SystemExit("Refusing write: PowerShell is required for the RPC chain-ID check")
        ps = (
            "$body = '{\"jsonrpc\":\"2.0\",\"method\":\"eth_chainId\",\"params\":[],\"id\":1}'; "
            f"$res = Invoke-RestMethod -Uri '{RPC}' -Method Post -ContentType 'application/json' -Body $body; "
            "if ($res.result -ne '0xf22f') { throw \"Unexpected chain ID: $($res.result)\" }; "
            "[Console]::WriteLine($res.result)"
        )
        check = subprocess.run([powershell, "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=30)
        if check.returncode or check.stdout.strip().lower() != "0xf22f":
            raise SystemExit("Refusing write: PowerShell RPC eth_chainId check failed: " + (check.stderr or check.stdout))
        result = check.stdout.strip()
    else:
        request = urllib.request.Request(
            RPC,
            data=json.dumps({"jsonrpc": "2.0", "method": "eth_chainId", "params": [], "id": 1}).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read())
        result = payload.get("result", "").lower()
        if result != "0xf22f":
            raise SystemExit(f"Refusing write: RPC chain ID is {result!r}, expected 0xf22f")
    print(f"Verified CLI studionet chainId={CHAIN_ID} and RPC eth_chainId={result}")


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit("Usage: python scripts/studionet_write.py <contract> <method> [arg ...] [--expect-rejection <text>]")
    contract, method, *args = sys.argv[1:]
    expected_rejection = None
    if "--expect-rejection" in args:
        index = args.index("--expect-rejection")
        if index + 1 >= len(args):
            raise SystemExit("--expect-rejection needs a reason substring")
        expected_rejection = args[index + 1]
        args = args[:index]
    verify_network()
    output = run(cli(["write", contract, method, "--rpc", RPC, "--args", *args]))
    match = re.search(r"Write Transaction Hash:\s*(0x[0-9a-fA-F]{64})", output)
    if not match:
        raise SystemExit("Write command returned no transaction hash:\n" + output[-12000:])
    tx_hash = match.group(1)
    receipt = run(cli(["receipt", tx_hash]), timeout=900)
    if "status_name: 'FINALIZED'" not in receipt and 'status_name: "FINALIZED"' not in receipt:
        raise SystemExit(f"Transaction {tx_hash} did not report FINALIZED:\n" + receipt[-12000:])
    if "result_name: 'MAJORITY_AGREE'" not in receipt:
        raise SystemExit(f"Transaction {tx_hash} did not finalize with majority agreement:\n" + receipt[-12000:])
    payload = re.search(r"payload:\s*'([^']*)'", receipt)
    rejection = payload.group(1) if payload else ""
    if expected_rejection is not None:
        if "execution_result: 'ERROR'" not in receipt or expected_rejection not in rejection:
            raise SystemExit(f"Transaction {tx_hash} did not produce expected rejection {expected_rejection!r}:\n" + receipt[-12000:])
        print(f"REJECTED {tx_hash} reason={rejection}")
        return
    if "execution_result: 'SUCCESS'" not in receipt:
        raise SystemExit(f"Transaction {tx_hash} finalized with an execution error ({rejection or 'no payload'}):\n" + receipt[-12000:])
    print(f"FINALIZED {tx_hash} {contract}.{method}")
    # Expose the actual transaction output for return-value inspection while
    # keeping the large validator traces out of routine logs.
    result = re.search(r"'result':\s*([^,\n]+)", receipt)
    if result:
        print("Receipt result:", result.group(1).strip())


if __name__ == "__main__":
    main()
