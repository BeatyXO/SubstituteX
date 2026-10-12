import pytest
import os

@pytest.fixture(autouse=True)
def _reset_registry(monkeypatch):
    # genlayer-test 0.29.2 keeps the temp message file open as fd 0, then
    # unlinks it immediately. Windows refuses that unlink until direct_vm
    # restores stdin during fixture teardown. Defer only that Windows case.
    original_unlink = os.unlink
    deferred = []

    def unlink(path, *args, **kwargs):
        try:
            return original_unlink(path, *args, **kwargs)
        except PermissionError:
            if os.name == "nt":
                deferred.append((path, args, kwargs))
                return None
            raise

    monkeypatch.setattr(os, "unlink", unlink)
    yield
    monkeypatch.setattr(os, "unlink", original_unlink)
    for path, args, kwargs in deferred:
        try:
            original_unlink(path, *args, **kwargs)
        except FileNotFoundError:
            pass
    try:
        import genlayer.gl.genvm_contracts as contracts
        contracts.__known_contract__ = None
    except ImportError:
        pass
