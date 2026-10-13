import pytest
import os
import gc

_DEFERRED_TEMP_UNLINKS = []

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
        except PermissionError:
            _DEFERRED_TEMP_UNLINKS.append((original_unlink, path, args, kwargs))
    try:
        import genlayer.gl.genvm_contracts as contracts
        contracts.__known_contract__ = None
    except ImportError:
        pass


def pytest_sessionfinish(session, exitstatus):
    """Retry Direct Mode's Windows stdin temp-file cleanup after fixture teardown."""
    if not _DEFERRED_TEMP_UNLINKS:
        return
    gc.collect()
    remaining = []
    for unlink, path, args, kwargs in _DEFERRED_TEMP_UNLINKS:
        try:
            unlink(path, *args, **kwargs)
        except FileNotFoundError:
            pass
        except PermissionError:
            remaining.append(path)
    if remaining:
        raise RuntimeError("Direct Mode temporary files remained locked: " + ", ".join(remaining))


@pytest.fixture(autouse=True)
def _optional_pickling_audit(request):
    """Enable genlayer-test's serialization audit on demand for lifecycle tests."""
    if os.environ.get("SUBSTITUTEX_CHECK_PICKLING") != "1":
        yield
        return
    direct_vm = request.getfixturevalue("direct_vm")
    direct_vm.check_pickling = True
    try:
        yield
    finally:
        direct_vm.check_pickling = False
